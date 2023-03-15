with
  bsee_well_assets as (
    select
      'bsee-jason-well-' || substr(API_WELL_NUMBER, 1, 10) as externalId,
      'bsee-jason-root-well' as parentExternalId,
      WELL_NAME as name,
      WELL_TYPE_CODE as description,
      'Well' as type,
      'bsee' as source,
      dataset_id('bsee:jason:dataset') as dataSetId,
      array('label-bsee', 'label-bsee-well') as labels,
      *
    from
      `bsee:jason:rawdb`.`well-header-prep`
  )
select
  externalId,
  parentExternalId,
  dataSetId,
  name,
  description,
  source,
  labels,
  to_metadata_except(
    array(
      "name",
      "externalId",
      "parentExternalId",
      "parentId",
      "dataSetId",
      "description",
      "key"
    ),
    *
  ) as metadata
from
  bsee_well_assets