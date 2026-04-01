\set ON_ERROR_STOP on

SELECT
  'Q9' AS query_id,
  count(*) AS row_count,
  round(sum(extendedprice * (1 - discount))::numeric, 2) AS revenue
FROM hd03_tpch.lineitem_smoke
WHERE shipdate >= DATE '1995-01-01';
