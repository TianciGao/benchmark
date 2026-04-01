\set ON_ERROR_STOP on

SELECT
  'Q21' AS query_id,
  l.returnflag,
  count(*) AS line_count
FROM hd03_tpch.lineitem_smoke AS l
GROUP BY l.returnflag
ORDER BY l.returnflag;
