\set ON_ERROR_STOP on

SELECT
  'Q64' AS query_id,
  d.d_moy,
  round(sum(ss.net_paid)::numeric, 2) AS net_paid_total
FROM hd03_tpcds.store_sales_smoke AS ss
JOIN hd03_tpcds.date_dim_smoke AS d
  ON d.d_date_sk = ss.sold_date_sk
GROUP BY d.d_moy
ORDER BY d.d_moy;
