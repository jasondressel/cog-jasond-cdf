from cognite.client import CogniteClient
from cdf.client import CDFConfig, Client
from pandas import DataFrame
from cognite.client.data_classes.raw import Row
from uuid import uuid4
from dotenv import load_dotenv
import os
from cognite.extractorutils.uploader import RawUploadQueue

def OpenAPI():

    CLIENT_ID = "1b90ede3-271e-401b-81a0-a4d52bea3273"
    CLIENT_SECRET = "jfR8Q~i.U8UktAKHKlkfCXFRb5P4zD7M8qUcpa1N"
    TENANT_ID = "48d5043c-cf70-4c49-881c-c638f5796997"
    CDF_CLUSTER = "api"
    CDF_PROJECT = "publicdata"

    open_api = CDFConfig(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        tenant_id=TENANT_ID,
        cdf_cluster=CDF_CLUSTER,
        cdf_project=CDF_PROJECT
    )

    client: CogniteClient = Client(open_api)
    # print(client.config)
    return client

def GetClient():
    load_dotenv()

    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    TENANT_ID = os.getenv('TENANT_ID')
    CDF_CLUSTER = os.getenv('CDF_CLUSTER')
    CDF_PROJECT = os.getenv('CDF_PROJECT')

    pemex_dev = CDFConfig(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        tenant_id=TENANT_ID,
        cdf_cluster=CDF_CLUSTER,
        cdf_project=CDF_PROJECT
    )

    client: CogniteClient = Client(pemex_dev)
    # print(client.config)
    return client


def EnsureRaw(client: CogniteClient, database: str, table: str, drop=False):
    """
    Ensure CDF database table exists
    """
    
    if drop:
        try:
            client.raw.tables.delete(db_name=database, name=table)
        except Exception as e:
            pass
     
    try:
        client.raw.databases.create(name=database)
    except Exception as e:
        pass


    try:
        client.raw.tables.create(db_name=database, name=table)
    except Exception as e:
        pass


def LoadRawQueue(
    dataFrame: DataFrame,
    database: str,
    table: str,
    totalRows: int,
    sourcename: str,
    rowKey="uuid4"):

    client = GetClient()
    batch_size=10000

    # Ensure the target database and tables exist
    EnsureRaw(client, database, table, False)

    cdf_database = f"{database} - table: {table}"
    print(f'Loading: {sourcename} to {cdf_database}')

    with RawUploadQueue(cdf_client=client, max_upload_interval=30, max_queue_size=100_000) as queue:
        for i, row in enumerate(dataFrame.iterrows(), start=1):
            values = row[1].fillna('').to_dict()
            key = uuid4().hex if rowKey == "uuid4" else values[rowKey]
            queue.add_to_upload_queue(database, table, Row(key=key, columns=values))
            if i % batch_size == 0:
                print(f'Queuing: {sourcename}: {i} of {totalRows}')
        print(f'QUEUED: {sourcename} {i} of {totalRows}')