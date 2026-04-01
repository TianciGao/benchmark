\set ON_ERROR_STOP on

-- HD-03 scaffolding only: placeholder local entry point for a future TPC-H load/refresh step.
-- Expected psql variables: data_dir, scale
SELECT
  'hd03_load_anchor_tpch_placeholder' AS scaffold_id,
  :'data_dir' AS data_dir,
  :'scale' AS scale;
