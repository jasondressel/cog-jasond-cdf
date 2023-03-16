from re import T
import pandas as pd
import time
import os
from tenacity import retry, wait_fixed, wait_random_exponential, stop_after_attempt, retry_if_exception_type
from pandas import DataFrame
from cognite.client.data_classes.raw import Row
from cognite.client.exceptions import CogniteReadTimeout

from datetime import datetime
from cdf.utils import GetClient
from cognite.client import CogniteClient
from cognite.client.utils import timestamp_to_ms


timeseries_names = [
    "MON_O_PROD_VOL",
    "MON_G_PROD_VOL",
    "MON_WTR_PROD_VOL",
    "WELL_STAT_CD",
    "DAYS_ON_PROD",
    "INJECTION_VOLUME"
]


#@retry(stop=stop_after_attempt(10), retry=(retry_if_exception_type(CogniteReadTimeout)), wait=wait_random_exponential())
def LoadRaw(dataFrame: DataFrame):
    batch_size=1000
    numRows = dataFrame.index.size
    database = "bsee:timeseries:rawdb"
    table = "timeseries_header"
    client: CogniteClient = GetClient()

    batch = []
    for i, row in enumerate(dataFrame.iterrows(), start=1):
        values = row[1].fillna('').to_dict()

        for timeseries in timeseries_names:
            key = f'{timeseries}-{values["API_WELL_NUMBER"]}-{values["COMPLETION_NAME"].strip()}'
            batch.append(Row(key=key, columns=values))

        if i % batch_size == 0:
            client.raw.rows.insert(db_name=database, table_name=table, row=batch)
            print(f'Loading: {i} of {numRows}')
            batch.clear()

    if batch:
        client.raw.rows.insert(db_name=database, table_name=table, row=batch)
        print(f'Loaded: {i} of {numRows}')
        batch.clear()


years = range(2022, 1995, -1)
cwd = os.getcwd()
files = [f'{cwd}/cdf/bsee/data/timeseries/ogora{y}delimit.txt' for y in years]
files.insert(0, f'{cwd}/cdf/bsee/data/timeseries/ogoradelimit.txt') # current year

tic = time.perf_counter()

totalRows = 0
dataFrames = []

for f in files:
    print(f'Loading file {f} . . .')
    ttic = time.perf_counter()

    dataFrame = pd.read_csv(f, dtype=str, encoding='latin1', header=None)
    dataFrame = dataFrame.astype(str)

    dataFrame.columns = [
        "LEASE_NUMBER",
        "COMPLETION_NAME",
        "PRODUCTION_DATE",
        "DAYS_ON_PROD",
        "PRODUCT_CODE",
        "MON_O_PROD_VOL",
        "MON_G_PROD_VOL",
        "MON_WTR_PROD_VOL",
        "API_WELL_NUMBER",
        "WELL_STAT_CD",
        "LEASE_AREA_BLOCK",
        "OPERATOR_NUM",
        "SORT_NAME",
        "FIELD_NAME_CODE",
        "INJECTION_VOLUME",
        "PROD_INTERVAL_CD",
        "FIRST_PROD_DATE",
        "UNIT_AGT_NUMBER",
        "UNIT_ALOC_SUFFIX"
    ]

    dataFrames.append(dataFrame)

    ttoc = time.perf_counter()
    rows = dataFrame.index.size
    totalRows = totalRows + rows

    print(f"Loaded {rows} rows in {ttoc - ttic:0.4f} seconds")


all_frames = pd.concat(dataFrames, axis=0, ignore_index=True)
toc = time.perf_counter()
print(f"Loaded {totalRows} rows in {toc - tic:0.4f} seconds")

# what are the unique producing completions in the dataset
unique = all_frames.drop_duplicates(subset=['API_WELL_NUMBER', 'COMPLETION_NAME'], keep='last')

# strip the measurement columns out
to_upload = unique.drop(columns=[
    "MON_O_PROD_VOL",
    "MON_G_PROD_VOL",
    "MON_WTR_PROD_VOL",
    "WELL_STAT_CD",
    "DAYS_ON_PROD",
    "INJECTION_VOLUME",
    "PRODUCTION_DATE"
])

LoadRaw(to_upload)