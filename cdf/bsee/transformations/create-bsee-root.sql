-- This transformation will create the Root Asset
select
  "BSEE USERNAME" as name,
  "bsee-USERNAME-root" as externalId,
  "USERNAME's BSEE Root Asset" as description,
  dataset_id("bsee:USERNAME:dataset") as dataSetId