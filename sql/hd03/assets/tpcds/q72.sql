\set ON_ERROR_STOP on

SELECT
  'Q72' AS query_id,
  count(*) AS row_count,
  round(avg(ss.sales_price)::numeric, 2) AS avg_sales_price
FROM hd03_tpcds.store_sales_smoke AS ss;
