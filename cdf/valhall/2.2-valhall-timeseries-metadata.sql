select
  concat("jason-valhall-", externalId) as externalId,
  name,
  description,
  unit as unit,
  cast(isStep as boolean) as isStep,
  cast(isString as boolean) as isString,
  to_metadata_except(array("id"), *) as metadata,
  dataset_id("bsee:jason:dataset") as dataSetId
from
  `bsee:jason:rawdb`.`valhall:pi_timeseries`