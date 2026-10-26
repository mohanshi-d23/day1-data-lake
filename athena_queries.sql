-- TO CREATE ACTUAL SQL TABLE IN DB WHICH WAS NEVER DONE BY GLUE (IT JUST STORES METADATA)
CREATE EXTERNAL TABLE `ev-db`.raw_csv (
  vin string,
  county string,
  city string,
  state string,
  postal_code string,
  model_year string,
  make string,
  model string,
  ev_type string,
  cafv_eligibility string,
  electric_range string,
  legislative_district string,
  dol_vehicle_id string,
  vehicle_location string,
  electric_utility string,
  geoid2020 string
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES ('separatorChar' = ',', 'quoteChar' = '"', 'escapeChar' = '\\')
STORED AS TEXTFILE
LOCATION 's3://mohanshi-mini-datalake-2026/raw/'
TBLPROPERTIES ('skip.header.line.count' = '1');


-- TO select first 2 rows
SELECT * FROM "ev-db"."raw_csv" LIMIT 2;

-- Same query on raw and curated data
SELECT make, COUNT(*) AS vehicles
FROM "ev-db"."raw_csv"      --raw_csv and raw are different
GROUP BY make
ORDER BY vehicles DESC
LIMIT 10;

SELECT make, COUNT(*) AS vehicles
FROM "ev-db"."curated"
GROUP BY make
ORDER BY vehicles DESC
LIMIT 10;

----------------SOME QUERIES-----------------------------
-- top10_makes
SELECT make, COUNT(*) AS vehicles
FROM "ev-db"."curated"
GROUP BY make
ORDER BY vehicles DESC
LIMIT 10;

-- by_model_year
SELECT model_year, COUNT(*) AS vehicles
FROM "ev-db"."curated"
GROUP BY model_year
ORDER BY model_year;

--range_outliers
SELECT vin_1_10, make, model, model_year, electric_range
FROM "ev-db"."curated"
WHERE electric_range > (
  SELECT approx_percentile(electric_range, 0.99) FROM "ev-db"."curated"
)
ORDER BY electric_range DESC
LIMIT 20;
