\set ON_ERROR_STOP on

SELECT
  'Q18' AS query_id,
  c.c_name,
  o.o_orderkey,
  o.o_totalprice,
  round(sum(l.l_quantity)::numeric, 2) AS total_quantity
FROM hd03_tpch.customer AS c
JOIN hd03_tpch.orders AS o
  ON c.c_custkey = o.o_custkey
JOIN hd03_tpch.lineitem AS l
  ON o.o_orderkey = l.l_orderkey
GROUP BY c.c_name, o.o_orderkey, o.o_totalprice
HAVING sum(l.l_quantity) > 100
ORDER BY o.o_totalprice DESC, o.o_orderkey;
