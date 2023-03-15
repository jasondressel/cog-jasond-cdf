from cognite.client import CogniteClient
from cognite.client.config import ClientConfig
from cognite.client.credentials import OAuthClientCredentials
from cognite.experimental import CogniteClient as ExperimentalCogniteClient
from pydantic import BaseModel


class CDFConfig(BaseModel):
    client_id: str
    client_secret: str
    tenant_id: str
    cdf_cluster: str
    cdf_project: str


def Client(cdfConfig: CDFConfig, debug: bool = False, max_workers: int = None) -> CogniteClient:
    clientConfig = ClientConfig(
        client_name=f"{cdfConfig.cdf_project}-client",
        project=cdfConfig.cdf_project,
        base_url=f"https://{cdfConfig.cdf_cluster}.cognitedata.com",
        debug=debug,
        max_workers=max_workers,
        credentials=OAuthClientCredentials(
            token_url=f"https://login.microsoftonline.com/{cdfConfig.tenant_id}/oauth2/v2.0/token",
            client_id=cdfConfig.client_id,
            client_secret=cdfConfig.client_secret,
            scopes=[f"https://{cdfConfig.cdf_cluster}.cognitedata.com/.default"])
    )
    return CogniteClient(clientConfig)
 

def ExperimentalClient(cdfConfig: CDFConfig, debug: bool = False, max_workers: int = None) -> ExperimentalCogniteClient:
    clientConfig = ClientConfig(
        client_name=f"{cdfConfig.cdf_project}-client",
        project=cdfConfig.cdf_project,
        base_url=f"https://{cdfConfig.cdf_cluster}.cognitedata.com",
        debug=debug,
        max_workers=max_workers,
        credentials=OAuthClientCredentials(
            token_url=f"https://login.microsoftonline.com/{cdfConfig.tenant_id}/oauth2/v2.0/token",
            client_id=cdfConfig.client_id,
            client_secret=cdfConfig.client_secret,
            scopes=[f"https://{cdfConfig.cdf_cluster}.cognitedata.com/.default"])
    )
    return ExperimentalCogniteClient(clientConfig)


from dotenv import load_dotenv
import os

def main():
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

    c: CogniteClient = Client(pemex_dev)
    print(c.config)

    ec: ExperimentalCogniteClient = ExperimentalClient(pemex_dev)
    print(ec.config)

if __name__ == "__main__":
   main()