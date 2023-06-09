from dataclasses import dataclass
from typing import List
import csv
from concurrent.futures.thread import ThreadPoolExecutor
from threading import Event

from cognite.client import CogniteClient
from cognite.client.data_classes import Row
from cognite.extractorutils import Extractor
from cognite.extractorutils.statestore import AbstractStateStore
from cognite.extractorutils.uploader import RawUploadQueue
from cognite.extractorutils.configtools import BaseConfig, RawDestinationConfig


@dataclass
class ExtractorConfig:
    """
    Configuration for the running extractor, so any performance tuning parameters should go here
    """
    upload_queue_size: int = 50000
    parallelism: int = 10


@dataclass
class FileConfig:
    """
    Source configuration, describing a CSV file, and where to put it in CDF
    """
    path: str
    key_column: str
    destination: RawDestinationConfig


@dataclass
class CsvConfig(BaseConfig):
    """
    Master configuration class, containing everything from the BaseConfig class, in addition to the custom building
    blocks defined above
    """
    files: List[FileConfig]
    extractor: ExtractorConfig = ExtractorConfig()


def extract_file(file: FileConfig, queue: RawUploadQueue) -> None:
    """
    Extract a single CSV file

    Args:
        file: Description of file to extract
        queue: Upload queue for batching RAW requests
    """
    print(f"Extracting content from {file.path} to {file.destination.database}/{file.destination.table}")

    try:
        with open(file.path) as infile:
            reader = csv.DictReader(infile, delimiter=",")

            for row in reader:
                queue.add_to_upload_queue(
                    database=file.destination.database,
                    table=file.destination.table,
                    raw_row=Row(key=row[file.key_column], columns=row),
                )

    except Exception as e:
        print(f"Extraction failed : {e}")


def run(cognite: CogniteClient, states: AbstractStateStore, config: CsvConfig, stop_event: Event) -> None:
    """
    Extract all files listed in configuration

    Args:
        cognite: Initialized cognite client object
        states: Initialized state store object
        config: Configuration parameters
        stop_event: Cancellation token, will be set when an interrupt signal is sent to the extractor process
    """
    with RawUploadQueue(
        cdf_client=cognite, max_upload_interval=30, max_queue_size=100_000
    ) as queue, ThreadPoolExecutor(
        max_workers=config.extractor.parallelism, thread_name_prefix="CsvExtractor"
    ) as executor:
        for file in config.files:
            if stop_event.is_set():
                break
            executor.submit(extract_file, file, queue)


def main(config_file_path: str = "./cdf/bsee/borehole_extractor_config.yaml") -> None:
    """
    Main entrypoint.

    Args:
        config_file_path: path to config file. Defaults to ./cdf/bsee/borehole_extractor_config.yaml
    """
    with Extractor(
        name="csv_extractor",
        description="An extractor that uploads CSV files to CDF Staging",
        config_class=CsvConfig,
        run_handle=run,
        config_file_path=config_file_path,
        use_default_state_store=False
    ) as extractor:
        extractor.run()


if __name__ == "__main__":
    main()