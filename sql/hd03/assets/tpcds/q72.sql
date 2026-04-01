\set ON_ERROR_STOP on

SELECT
  'Q72' AS query_id,
  ca.ca_state,
  round(avg(ss.ss_sales_price)::numeric, 2) AS avg_sales_price,
  count(*) AS sales_count
FROM hd03_tpcds.store_sales AS ss
JOIN hd03_tpcds.customer AS c
  ON c.c_customer_sk = ss.ss_customer_sk
JOIN hd03_tpcds.customer_address AS ca
  ON ca.ca_address_sk = c.c_current_addr_sk
GROUP BY ca.ca_state
ORDER BY ca.ca_state;
