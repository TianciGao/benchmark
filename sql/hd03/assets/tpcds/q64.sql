\set ON_ERROR_STOP on

SELECT
  'Q64' AS query_id,
  d.d_year,
  i.i_class,
  round(sum(ss.ss_net_paid)::numeric, 2) AS net_paid_total
FROM hd03_tpcds.store_sales AS ss
JOIN hd03_tpcds.item AS i
  ON i.i_item_sk = ss.ss_item_sk
JOIN hd03_tpcds.date_dim AS d
  ON d.d_date_sk = ss.ss_sold_date_sk
GROUP BY d.d_year, i.i_class
ORDER BY d.d_year, i.i_class;
