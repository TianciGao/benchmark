\set ON_ERROR_STOP on

SELECT
  'Q21' AS query_id,
  s.s_name,
  count(*) AS wait_count
FROM hd03_tpch.supplier AS s
JOIN hd03_tpch.lineitem AS l1
  ON s.s_suppkey = l1.l_suppkey
JOIN hd03_tpch.orders AS o
  ON o.o_orderkey = l1.l_orderkey
JOIN hd03_tpch.nation AS n
  ON n.n_nationkey = s.s_nationkey
WHERE o.o_orderstatus = 'F'
  AND n.n_name = 'CANADA'
  AND EXISTS (
    SELECT 1
    FROM hd03_tpch.lineitem AS l2
    WHERE l2.l_orderkey = l1.l_orderkey
      AND l2.l_suppkey <> l1.l_suppkey
  )
GROUP BY s.s_name
ORDER BY wait_count DESC, s.s_name;
