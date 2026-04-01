\set ON_ERROR_STOP on

SELECT
  'Q18' AS query_id,
  o.orderpriority,
  count(*) AS orders_seen,
  round(sum(o.totalprice)::numeric, 2) AS total_revenue
FROM hd03_tpch.orders_smoke AS o
GROUP BY o.orderpriority
ORDER BY o.orderpriority;
