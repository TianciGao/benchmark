\set ON_ERROR_STOP on

SELECT
  'Q9' AS query_id,
  n.n_name AS nation,
  round(sum(l.l_extendedprice * (1 - l.l_discount) - ps.ps_supplycost * l.l_quantity)::numeric, 2) AS amount
FROM hd03_tpch.part AS p
JOIN hd03_tpch.lineitem AS l
  ON p.p_partkey = l.l_partkey
JOIN hd03_tpch.supplier AS s
  ON s.s_suppkey = l.l_suppkey
JOIN hd03_tpch.partsupp AS ps
  ON ps.ps_partkey = l.l_partkey
 AND ps.ps_suppkey = l.l_suppkey
JOIN hd03_tpch.orders AS o
  ON o.o_orderkey = l.l_orderkey
JOIN hd03_tpch.nation AS n
  ON n.n_nationkey = s.s_nationkey
WHERE p.p_name LIKE '%green%'
GROUP BY n.n_name
ORDER BY n.n_name;
