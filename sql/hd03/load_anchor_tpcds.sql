\set ON_ERROR_STOP on

-- HD-03 scaffolding only: placeholder local entry point for a future TPC-DS load/refresh step.
-- Expected psql variables: data_dir, scale
SELECT
  'hd03_load_anchor_tpcds_placeholder' AS scaffold_id,
  :'data_dir' AS data_dir,
  :'scale' AS scale;
