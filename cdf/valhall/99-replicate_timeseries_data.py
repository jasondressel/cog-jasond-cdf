from cognite.client import CogniteClient
from cognite.client.data_classes import Datapoint, Datapoints
from cognite.client.exceptions import CogniteAPIError

from cognite.client.utils._time import timestamp_to_ms
import csv
from cdf.utils import GetClient, OpenAPI

from typing import Any, Callable, List, Optional, Tuple, Union
from datetime import datetime, timedelta

source = OpenAPI()
target = GetClient()


def _get_time_range(src_datapoint: Datapoints, dst_datapoint: Datapoints) -> Tuple[int, int]:
    # +1 because datapoint retrieval time ranges are inclusive on start and exclusive on end
    start_time = 0 if not dst_datapoint else dst_datapoint.timestamp[0] + 1
    end_time = 0 if not src_datapoint else src_datapoint.timestamp[0] + 1
    return start_time, end_time


def replicate_historical_datapoints(
    client_src: CogniteClient,
    client_dst: CogniteClient,
    ts_external_id: str,
    mock_run = False,
    limit: Optional[int] = None,
    partition_size: int = 100000,
    start: Union[int, str] = None,
    end: Union[int, str] = None,
    days: int = -365
) -> Tuple[str, bool, int]:
    latest_dst_dp = client_dst.datapoints.retrieve_latest(external_id=ts_external_id)
    latest_src_dp = client_src.datapoints.retrieve_latest(external_id=ts_external_id)

    if not latest_src_dp:
        return ts_external_id, True, 0

    _start, _end = _get_time_range(latest_src_dp, latest_dst_dp)

    start = _start if start is None else timestamp_to_ms(start)
    end = _end if end is None else timestamp_to_ms(end)

    # adjust start to be just 1 year historical
    _enddt = datetime.fromtimestamp(end/1000)
    _startdt = _enddt + timedelta(days=days)
    _start = datetime.timestamp(_startdt) * 1000
    start = max(start, _start)

    # API Restrictions
    start = max(start, 31536000000)  # 1971

    print(f"external_id: {ts_external_id} Retrieving datapoints between {_startdt} and {_enddt}")
    datapoints_count = 0
    while start < end:
        num_to_fetch = partition_size if limit is None else min(partition_size, limit - datapoints_count)
        if num_to_fetch == 0:
            break

        try:
            datapoints = client_src.datapoints.retrieve(
                external_id=ts_external_id,
                start=start, 
                end=end,
                limit=num_to_fetch)
            
            if not datapoints:
                break

            if not mock_run:
                client_dst.datapoints.insert(datapoints, external_id=ts_external_id)
        except CogniteAPIError as exc:
            print(f"Failed: external id {ts_external_id}. {exc}")
            return ts_external_id, False, datapoints_count
        else:
            datapoints_count += len(datapoints)
            start = datapoints[-1].timestamp + 1

    result = (ts_external_id, True, datapoints_count)
    print(f"Completed {result}")
    return result

time_series = target.time_series.list(external_id_prefix="pi:", limit=None)

from multiprocessing.pool import ThreadPool
pool = ThreadPool(16)

args = [(source, target, t.external_id, False) for t in time_series]
results = []
results = pool.starmap(replicate_historical_datapoints, args)