select
  concat("jason-valhall-", id) as externalId,
  if(
    parentId = "",
    parentId,
    concat("jason-valhall-", parentId)
  ) as parentExternalId,
  'Open Industrial Data' as source,
  name,
  description,
  to_metadata_except(array("id", "parentId"), *) as metadata,
  dataset_id("bsee:jason:dataset") as dataSetId
from
  `bsee:jason:rawdb`.`valhall:assets`