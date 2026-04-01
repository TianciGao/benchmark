\set ON_ERROR_STOP on

SELECT
  'Q95' AS query_id,
  i.i_category,
  max(ss.ss_quantity) AS max_quantity,
  round(sum(ss.ss_net_paid)::numeric, 2) AS total_net_paid
FROM hd03_tpcds.store_sales AS ss
JOIN hd03_tpcds.item AS i
  ON i.i_item_sk = ss.ss_item_sk
GROUP BY i.i_category
ORDER BY i.i_category;
