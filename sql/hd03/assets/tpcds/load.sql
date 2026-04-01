\set ON_ERROR_STOP on

BEGIN;

TRUNCATE TABLE hd03_tpcds.store_sales_smoke;
TRUNCATE TABLE hd03_tpcds.date_dim_smoke;

INSERT INTO hd03_tpcds.pilot_metadata (benchmark, scale, data_dir, loaded_at)
VALUES ('tpcds', :'scale', :'data_dir', now())
ON CONFLICT (benchmark) DO UPDATE
SET scale = EXCLUDED.scale,
    data_dir = EXCLUDED.data_dir,
    loaded_at = EXCLUDED.loaded_at;

INSERT INTO hd03_tpcds.date_dim_smoke (d_date_sk, d_year, d_moy)
VALUES
  (1, 2001, 1),
  (2, 2001, 2),
  (3, 2001, 3)
ON CONFLICT (d_date_sk) DO UPDATE
SET d_year = EXCLUDED.d_year,
    d_moy = EXCLUDED.d_moy;

INSERT INTO hd03_tpcds.store_sales_smoke (
  sold_date_sk,
  item_sk,
  customer_sk,
  net_paid,
  quantity,
  sales_price
)
VALUES
  (1, 10001, 501, 125.00, 2, 62.50),
  (2, 10002, 502, 250.00, 4, 62.50),
  (3, 10003, 503, 310.00, 5, 62.00)
ON CONFLICT (sold_date_sk) DO UPDATE
SET item_sk = EXCLUDED.item_sk,
    customer_sk = EXCLUDED.customer_sk,
    net_paid = EXCLUDED.net_paid,
    quantity = EXCLUDED.quantity,
    sales_price = EXCLUDED.sales_price;

COMMIT;
