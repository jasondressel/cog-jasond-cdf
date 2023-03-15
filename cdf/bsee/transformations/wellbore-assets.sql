with
  bsee_wellbore_assets as (
    select
      'bsee-jason-wellbore-' || API_WELL_NUMBER as externalId,
      'bsee-jason-well-' || substr(API_WELL_NUMBER, 1, 10) as parentExternalId,
      WELL_NAME || '-' || WELL_NAME_SUFFIX as name,
      BOREHOLE_STAT_CD as description,
      'Wellbore' as type,
      'bsee' as source,
      dataset_id('bsee:jason:dataset') as dataSetId,
      array('label-bsee', 'label-bsee-wellbore') as labels,
      *
    from
        -- NOTE THAT WE ARE USING THE BOREHOLES TABLE
        `bsee:jason:rawdb`.`boreholes`
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
  bsee_wellbore_assets