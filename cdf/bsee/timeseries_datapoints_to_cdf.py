from re import T
import pandas as pd
import time
import os
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

years = range(1996, 2023, 1)
cwd = os.getcwd()
files = [f'{cwd}/cdf/bsee/data/timeseries/ogora{y}delimit.txt' for y in years]
files.append(f'{cwd}/cdf/bsee/data/timeseries/ogoradelimit.txt') # current year

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
print(f"Loaded {totalRows} totalrows in {toc - tic:0.4f} seconds")

# NOTE: This is brute force.  There's likely a better way
# what are the unique producing completions in the dataset
unique = all_frames.drop_duplicates(subset=['API_WELL_NUMBER', 'COMPLETION_NAME'], keep='last')

# prepopulate
datapoints = {}
for i in unique.index:
    for name in timeseries_names:
        key = f'{name}-{unique["API_WELL_NUMBER"][i]}-{unique["COMPLETION_NAME"][i].strip()}'
        datapoints[key] = [] # empty array

# populate
for i in all_frames.index:
    for name in timeseries_names:
        key = f'{name}-{all_frames["API_WELL_NUMBER"][i]}-{all_frames["COMPLETION_NAME"][i].strip()}'
        points = datapoints[key]
        points.append(
            (timestamp_to_ms(datetime.strptime(all_frames['PRODUCTION_DATE'][i], '%Y%m')), float(all_frames[name][i]))
        )


client = GetClient()
for key, value in datapoints.items():
    externalId = f'bsee-{key}'
    try:
        client.time_series.data.insert(external_id=externalId, datapoints=value)
    except:
        print(f"Failed to load {externalId}")
