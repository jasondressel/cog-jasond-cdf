from cdf.utils import GetClient
from cognite.client.data_classes.extractionpipelines import ExtractionPipeline

client = GetClient()

# create the prerequisite tables
client.raw.tables.create("bsee:jason:rawdb", "boreholes")

# create the borehole extractor pipeline
borehole_pipeline = ExtractionPipeline(
    external_id="extpipe-jason-borehole-extractor",
    name="BSEE Borehole Extraction Pipeline",
    data_set_id= 7633408842391360, # You need to get this from Fusion
    raw_tables=[{"dbName":"bsee:jason:rawdb", "tableName":"boreholes"}]
)

result = client.extraction_pipelines.create(borehole_pipeline)
print(result)