import os
from cognite.client.data_classes import ThreeDModelRevision
from cdf.utils import GetClient

cwd = os.getcwd()
file = f"{cwd}/cdf/valhall/data/Valhall_VPH_colored_converted_nwd_ciff.zip"

client = GetClient()

# create 3D Model
model = client.three_d.models.create(name = "Jason's Valhall VPH Colored")

# upload 3D file
valhall_model_file = client.files.upload(
    path=file,
    name='Valhall_VPH_colored_converted_nwd_ciff.zip',
    mime_type="application/octet-stream",
    source="Open Industrial Data",
    data_set_id=137409537563188,
    overwrite=True)

# create Model Revision
revision = client.three_d.revisions.create(
    model_id = model.id,
    revision=ThreeDModelRevision(
        file_id=valhall_model_file.id,
        published=False
    ))