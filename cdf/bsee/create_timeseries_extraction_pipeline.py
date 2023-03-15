from cdf.utils import GetClient
from cognite.client.data_classes.extractionpipelines import ExtractionPipeline

client = GetClient()

# create the prerequisite tables
client.raw.tables.create("bsee:timeseries:rawdb", "ogora")

# create the timeseries extractor pipeline
timeseries_pipeline = ExtractionPipeline(
    external_id="extpipe-jason-timeseries-extractor",
    name="BSEE Timeseries Extraction Pipeline",
    data_set_id= 137409537563188, # You need to get this from Fusion
    raw_tables=[{"dbName":"bsee:timeseries:rawdb", "tableName":"ogora"}]
)

result = client.extraction_pipelines.create(timeseries_pipeline)
print(result)