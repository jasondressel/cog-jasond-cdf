import glob
import os
from cdf.utils import GetClient

cwd = os.getcwd()
directory = f"{cwd}/cdf/valhall/data"
file_paths = glob.glob(f'{directory}/*.pdf')

client = GetClient()

for path in file_paths:
    print(path)

    client.files.upload(
        path=path,
        name=f'jason-{os.path.basename(path)}', # REPLACE WITH YOUR NAME
        mime_type="application/pdf",
        source="Open Industrial Data",
        data_set_id=7633408842391360, # REPLACE WITH YOUR DATASET ID
        overwrite=True)