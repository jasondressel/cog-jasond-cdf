select
  count(*) as wellbore_count,
  "Well" as type,
  substr(API_WELL_NUMBER, 1, 10) as key,
  substr(API_WELL_NUMBER, 1, 10) as API_WELL_NUMBER,
  first(SURF_LATITUDE) as SURF_LATITUDE,
  first(SURF_LONGITUDE) as SURF_LONGITUDE,
  first(SURF_LEASE_NUMBER) as SURF_LEASE_NUMBER,
  first(COMPANY_NAME) as COMPANY_NAME,
  first(WELL_NAME) as WELL_NAME,
  first(WELL_TYPE_CODE) as WELL_TYPE_CODE,
  first(WELL_SPUD_DATE) as WELL_SPUD_DATE,
  first(WATER_DEPTH) as WATER_DEPTH,
  first(RKB_ELEVATION) as RKB_ELEVATION
from
  -- ENSURE YOU HAVE THE CORRECT SOURCE TABLE
  `bsee:jason:rawdb`.`boreholes`
group by
  substr(API_WELL_NUMBER, 1, 10)
order by
  wellbore_count desc,
  API_WELL_NUMBER asc