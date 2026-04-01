\set ON_ERROR_STOP on

SELECT
  'Q95' AS query_id,
  max(ss.quantity) AS max_quantity,
  round(sum(ss.net_paid)::numeric, 2) AS total_net_paid
FROM hd03_tpcds.store_sales_smoke AS ss;
