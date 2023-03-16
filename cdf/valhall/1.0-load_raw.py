import pandas as pd
from uuid import uuid4
import os
from pandas import DataFrame
from cognite.client.data_classes.raw import Row

from cdf.utils import GetClient
from cognite.client import CogniteClient


def LoadRaw(
    client: CogniteClient,
    dataFrame: DataFrame,
    database: str,
    table: str,
    rowKey="uuid4",
    batch_size=10000):
    """
    Load DataFrame into CDF RAW table
    """
      
    # Ensure the target database and table exist
    try:
        client.raw.tables.create(db_name=database, name=table)
    except Exception as e:
        pass
    
    print(f'Loading database: {database} - table: {table}')
    batch = []
    for i, row in enumerate(dataFrame.iterrows(), start=1):
        values = row[1].fillna('').to_dict()            
        key = uuid4().hex if rowKey == "uuid4" else values[rowKey]
        batch.append(Row(key=key, columns=values))
        if i % batch_size == 0:
            client.raw.rows.insert(db_name=database, table_name=table, row=batch)
            batch.clear()

    if batch:
        client.raw.rows.insert(db_name=database, table_name=table, row=batch)
        batch.clear()


cwd = os.getcwd()
files_to_load = [
    ("valhall:assets", f"{cwd}/cdf/valhall/data/source_assets.csv", "id"),
    ("valhall:pi_timeseries", f"{cwd}/cdf/valhall/data/source_timeseries.csv", "id")
]

client = GetClient()

for f in files_to_load:
    table_name = f[0]
    file_name = f[1]
    dataFrame = pd.read_csv(file_name, dtype=str, encoding='latin1')
    rowkey = f[2]

    LoadRaw(
        client,
        dataFrame,
        "bsee:jason:rawdb",
        table_name,
        rowkey)