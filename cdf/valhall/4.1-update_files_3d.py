from cdf.utils import GetClient
from cognite.client.data_classes import FileMetadataList

# update the dataset id
client = GetClient()
files: FileMetadataList = client.files.list(limit=None)
for f in files:
    f.data_set_id = 137409537563188
client.files.update(files)