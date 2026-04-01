\set ON_ERROR_STOP on

BEGIN;

TRUNCATE TABLE hd03_tpch.lineitem CASCADE;
TRUNCATE TABLE hd03_tpch.partsupp CASCADE;
TRUNCATE TABLE hd03_tpch.orders CASCADE;
TRUNCATE TABLE hd03_tpch.customer CASCADE;
TRUNCATE TABLE hd03_tpch.part CASCADE;
TRUNCATE TABLE hd03_tpch.supplier CASCADE;
TRUNCATE TABLE hd03_tpch.nation CASCADE;

INSERT INTO hd03_tpch.pilot_metadata (benchmark, scale, data_dir, loaded_at)
VALUES ('tpch', :'scale', :'data_dir', now())
ON CONFLICT (benchmark) DO UPDATE
SET scale = EXCLUDED.scale,
    data_dir = EXCLUDED.data_dir,
    loaded_at = EXCLUDED.loaded_at;

INSERT INTO hd03_tpch.nation (n_nationkey, n_name)
VALUES
  (1, 'BRAZIL'),
  (2, 'CANADA')
ON CONFLICT (n_nationkey) DO UPDATE
SET n_name = EXCLUDED.n_name;

INSERT INTO hd03_tpch.supplier (s_suppkey, s_name, s_nationkey)
VALUES
  (10, 'Supplier#000000010', 1),
  (20, 'Supplier#000000020', 2)
ON CONFLICT (s_suppkey) DO UPDATE
SET s_name = EXCLUDED.s_name,
    s_nationkey = EXCLUDED.s_nationkey;

INSERT INTO hd03_tpch.part (p_partkey, p_name)
VALUES
  (100, 'green widget'),
  (200, 'blue widget')
ON CONFLICT (p_partkey) DO UPDATE
SET p_name = EXCLUDED.p_name;

INSERT INTO hd03_tpch.partsupp (ps_partkey, ps_suppkey, ps_supplycost)
VALUES
  (100, 10, 17.50),
  (100, 20, 19.00),
  (200, 10, 23.00)
ON CONFLICT (ps_partkey, ps_suppkey) DO UPDATE
SET ps_supplycost = EXCLUDED.ps_supplycost;

INSERT INTO hd03_tpch.customer (c_custkey, c_name)
VALUES
  (1000, 'Customer#000001000'),
  (2000, 'Customer#000002000')
ON CONFLICT (c_custkey) DO UPDATE
SET c_name = EXCLUDED.c_name;

INSERT INTO hd03_tpch.orders (
  o_orderkey,
  o_custkey,
  o_orderstatus,
  o_totalprice,
  o_orderdate,
  o_orderpriority
)
VALUES
  (1, 1000, 'O', 1000.00, DATE '1995-01-10', '1-URGENT'),
  (2, 2000, 'F', 2500.00, DATE '1995-02-10', '2-HIGH'),
  (3, 1000, 'O', 3100.00, DATE '1995-03-10', '3-MEDIUM')
ON CONFLICT (o_orderkey) DO UPDATE
SET o_custkey = EXCLUDED.o_custkey,
    o_orderstatus = EXCLUDED.o_orderstatus,
    o_totalprice = EXCLUDED.o_totalprice,
    o_orderdate = EXCLUDED.o_orderdate,
    o_orderpriority = EXCLUDED.o_orderpriority;

INSERT INTO hd03_tpch.lineitem (
  l_orderkey,
  l_partkey,
  l_suppkey,
  l_linenumber,
  l_quantity,
  l_extendedprice,
  l_discount,
  l_returnflag,
  l_linestatus,
  l_shipdate,
  l_receiptdate,
  l_commitdate
)
VALUES
  (1, 100, 10, 1, 150.00, 1000.00, 0.05, 'N', 'O', DATE '1995-01-20', DATE '1995-01-28', DATE '1995-01-24'),
  (1, 100, 20, 2, 160.00, 1200.00, 0.04, 'N', 'O', DATE '1995-01-22', DATE '1995-01-30', DATE '1995-01-23'),
  (2, 200, 10, 1, 40.00, 600.00, 0.03, 'R', 'F', DATE '1995-02-20', DATE '1995-02-27', DATE '1995-02-21'),
  (2, 100, 20, 2, 25.00, 300.00, 0.02, 'R', 'F', DATE '1995-02-21', DATE '1995-02-28', DATE '1995-02-22'),
  (3, 100, 10, 1, 70.00, 900.00, 0.07, 'N', 'O', DATE '1995-03-20', DATE '1995-03-30', DATE '1995-03-25')
ON CONFLICT (l_orderkey, l_linenumber) DO UPDATE
SET l_partkey = EXCLUDED.l_partkey,
    l_suppkey = EXCLUDED.l_suppkey,
    l_quantity = EXCLUDED.l_quantity,
    l_extendedprice = EXCLUDED.l_extendedprice,
    l_discount = EXCLUDED.l_discount,
    l_returnflag = EXCLUDED.l_returnflag,
    l_linestatus = EXCLUDED.l_linestatus,
    l_shipdate = EXCLUDED.l_shipdate,
    l_receiptdate = EXCLUDED.l_receiptdate,
    l_commitdate = EXCLUDED.l_commitdate;

COMMIT;
