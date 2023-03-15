# Data Extraction

1. [Wells and Wellbores](#well-and-wellbore)
1.1 [Borehole Extraction Pipeline](#borehole-extraction-pipeline)
1.2 [Borehole Extractor](#borehole-extractor)
2. [Timeseries](#time-series)
3. [Lease](#lease-area-block)
4. [Company](#company)
5. [Lease Assignments](#lease-assignments)


## Well and Wellbore

- We pre-downloaded [BSEE Borehole data](https://www.data.bsee.gov/Main/Well.aspx) as [boreholes.csv](../cdf/bsee/data/boreholes.csv)
- Our primary goal is to ingest data into CDF Staging (RAW) storage within CDF. Ingesting data into RAW enables us to process and re-process data in various ways without pushing additional load on the original data sources. It's recommended to store all non-high-volume data in RAW before you process it within CDF.

#### Borehole Extraction Pipeline

To make sure you have reliable and trustworthy data ingestion into CDF Staging, we need to set up data sets to track the source, and extraction pipelines to monitor the data flow. Extraction pipelines also allow you to activate automatic email notifications to catch any extractor failures or data flow interruptions.
- For this workshop, we manually created the pipeline using [Cognite Python SDK](https://cognite-sdk-python.readthedocs-hosted.com/en/latest/cognite.html#extraction-pipelines).  [create_borehole_extraction_pipeline.py](../cdf/bsee/create_borehole_extraction_pipeline.py) creates this pipeline in CDF.

!!! NOTE: 
    You can create extraction pipelines via CLI: https://github.com/cognitedata/inso-extpipes-cli

!!! TODO 
    - Ensure you modify [create_borehole_extraction_pipeline.py](../cdf/bsee/create_borehole_extraction_pipeline.py) with your USERNAME
    - Use the correct DATASET_ID (you can find it via Fusion UI)
    - Run [create_borehole_extraction_pipeline.py](../cdf/bsee/create_borehole_extraction_pipeline.py)

    ```python
    # sample USERNAME substitution
    client = GetClient()

    # create the boreholes table
    client.raw.tables.create("bsee:jason:rawdb", "boreholes")

    # create the extractor pipeline
    borehole_pipeline = ExtractionPipeline(
        external_id="extpipe-jason-borehole-extractor",
        name="BSEE Borehole Extraction Pipeline",
        data_set_id=110000111110, # You need to get this from Fusion
        raw_tables=[{"dbName":"bsee:jason:rawdb", "tableName":"boreholes"}]
    )
    
    ``` 

#### Borehole Extractor
We created a sample custom extractor: [borehole-extractor.py](../cdf/bsee/borehole_extractor.py) which leverages [cognite-extractor-utils](https://cognite-extractor-utils.readthedocs-hosted.com/en/latest/index.html) python SDK.  

When executed, the [boreholes.csv](../cdf/bsee/data/boreholes.csv) file is read and pushed to CDF Staging (RAW).  This extractor has a corresponding [borehole_extractor_config.yaml](./../cdf/bsee/borehole_extractor_config.yaml) which is used to setup and configure target CDF project, connection credentials, source csv files and target CDF staging tables.

!!! TODO
    - Modify the target CDF database specified in the [borehole_extractor_config.yaml](./../cdf/bsee/borehole_extractor_config.yaml) file.
    - Run [borehole-extractor.py](../cdf/bsee/borehole_extractor.py)
    - Navigate to CDF Raw Explorer, you should see your boreholes table populated with 54928 rows

    ```yaml
    files:
        - path: ./cdf/bsee/data/boreholes.csv
            key-column: API_WELL_NUMBER
            destination:
            database: bsee:jason:rawdb  # Change this to your username
            table: boreholes
    ```

## Time Series
Time series have been pre-loaded via CSV's downloaded from [BSEE>>Data Center>>Production OGOR-A](https://www.data.bsee.gov/Main/OGOR-A.aspx)
- Monthly Production for the years 1996 - 2023 were downloaded and are located in [bsee\data\timeseries](./../cdf/bsee/data/timeseries) folder.
- [timeseries_extractor.py](./../cdf/bsee/timeseries_extractor.py) was used to read each file and load to CDF Raw
- Loading of the data was done with the help of [cognite-extracto-utils](https://cognite-extractor-utils.readthedocs-hosted.com/en/latest/index.html) python SDK. The extractor-utils package is an extension of the Cognite Python SDK intended to simplify the development of data extractors for Cognite Data Fusion.
- The data was loaded into a shared CDF Raw Database: [bsee:timeseries:rawdb](https://pemex.fusion.cognite.com/pemex-dev/raw?activeTable=%5B%22bsee%3Atimeseries%3Arawdb%22%2C%22ogora%22%2Cnull%5D&cluster=az-eastus-1.cognitedata.com&env=az-eastus-1&tabs=%5B%5B%22bsee%3Atimeseries%3Arawdb%22,%22ogora%22,null%5D%5D) so we do not need everyone to load the >41 Million rows of monthly production data.

## Lease Area Block

## Company

## Lease Assignments