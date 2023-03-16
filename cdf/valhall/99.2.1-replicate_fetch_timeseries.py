from cognite.client import CogniteClient
import cdf
import pandas

TENANT_ID = "b7ac094b-ffd9-4c96-a67d-eab64a07eca3"
CLIENT_ID = "fb81adb4-d9b8-4614-b717-c792c0303630"
CDF_CLUSTER = "bluefield"  # api, westeurope-1 etc
COGNITE_PROJECT = "jdblue"

SCOPES = [f"https://{CDF_CLUSTER}.cognitedata.com/.default"]
CLIENT_SECRET = ".Q-HEZDh_OoEh-aeG-T.96ULP2-A-Xv3~7"  # os.getenv("CLIENT_SECRET")  # store secret in env variable
TOKEN_URL = "https://login.microsoftonline.com/%s/oauth2/v2.0/token" % TENANT_ID

target = cdf.Client()
print(target.login.status)

source = CogniteClient(
    api_key="MjRiNDA2YTctYTQ1MC00MThiLWIxYWEtOWE0MTA0YmU4YWIy",
    project="publicdata",
    client_name="publicdata",
    base_url="https://api.cognitedata.com"
)
print(source.login.status)
resources = source.time_series.list(limit=None)

resources_pd = source.time_series.list(external_id_prefix="pi:", limit=None).to_pandas()
source_timeseries = pandas.concat([resources_pd.drop('metadata', axis=1), pandas.json_normalize(resources_pd['metadata'])], axis=1)
source_timeseries = source_timeseries.drop(['createdTime', 'lastUpdatedTime', '_replicatedTime', '_replicatedSource', '_replicatedInternalId', 'assetId'], axis=1)
file_path = f'/Users/jason.dressel/Code/jdblue/jdblue/valhall/data/source_timeseries.csv'

source_timeseries.to_csv(file_path, index=False)