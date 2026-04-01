\set ON_ERROR_STOP on

BEGIN;

TRUNCATE TABLE hd03_tpch.lineitem_smoke;
TRUNCATE TABLE hd03_tpch.orders_smoke;

INSERT INTO hd03_tpch.pilot_metadata (benchmark, scale, data_dir, loaded_at)
VALUES ('tpch', :'scale', :'data_dir', now())
ON CONFLICT (benchmark) DO UPDATE
SET scale = EXCLUDED.scale,
    data_dir = EXCLUDED.data_dir,
    loaded_at = EXCLUDED.loaded_at;

INSERT INTO hd03_tpch.orders_smoke (
  orderkey,
  custkey,
  orderstatus,
  totalprice,
  orderdate,
  orderpriority,
  clerk
)
VALUES
  (1, 101, 'O', 1000.00, DATE '1995-01-10', '1-URGENT', 'Clerk#000000001'),
  (2, 102, 'F', 2500.00, DATE '1995-02-10', '2-HIGH', 'Clerk#000000002'),
  (3, 103, 'O', 3100.00, DATE '1995-03-10', '3-MEDIUM', 'Clerk#000000003')
ON CONFLICT (orderkey) DO UPDATE
SET custkey = EXCLUDED.custkey,
    orderstatus = EXCLUDED.orderstatus,
    totalprice = EXCLUDED.totalprice,
    orderdate = EXCLUDED.orderdate,
    orderpriority = EXCLUDED.orderpriority,
    clerk = EXCLUDED.clerk;

INSERT INTO hd03_tpch.lineitem_smoke (
  orderkey,
  partkey,
  suppkey,
  quantity,
  extendedprice,
  discount,
  tax,
  returnflag,
  linestatus,
  shipdate
)
VALUES
  (1, 1001, 501, 17.00, 100.00, 0.05, 0.02, 'N', 'O', DATE '1995-01-20'),
  (2, 1002, 502, 36.00, 250.00, 0.04, 0.03, 'R', 'F', DATE '1995-02-20'),
  (3, 1003, 503, 22.00, 310.00, 0.07, 0.01, 'N', 'O', DATE '1995-03-20')
ON CONFLICT (orderkey) DO UPDATE
SET partkey = EXCLUDED.partkey,
    suppkey = EXCLUDED.suppkey,
    quantity = EXCLUDED.quantity,
    extendedprice = EXCLUDED.extendedprice,
    discount = EXCLUDED.discount,
    tax = EXCLUDED.tax,
    returnflag = EXCLUDED.returnflag,
    linestatus = EXCLUDED.linestatus,
    shipdate = EXCLUDED.shipdate;

COMMIT;
