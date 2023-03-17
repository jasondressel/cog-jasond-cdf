from cdf.utils import GetClient
from cognite.client.data_classes.time_series import TimeSeries

client = GetClient()

# s: TimeSeries
# for series in client.time_series(chunk_size=1000, data_set_external_ids="bsee:timeseries:dataset"):
#     update = []
#     for s in series:
#         s.data_set_id=6319614358687437  #bsee:all:dataset
#         update.append(s)
#     client.time_series.update(update)
#     update.clear()


s: TimeSeries
update = []

for series in client.time_series(chunk_size=1000, data_set_ids=[6319614358687437]):
    for s in series:
        if s.external_id.startswith('pi'):
            s.data_set_id=137409537563188  #bsee:timeseries:dataset
            update.append(s)
client.time_series.update(update)