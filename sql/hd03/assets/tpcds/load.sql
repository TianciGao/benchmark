\set ON_ERROR_STOP on

BEGIN;

TRUNCATE TABLE hd03_tpcds.store_sales CASCADE;
TRUNCATE TABLE hd03_tpcds.item CASCADE;
TRUNCATE TABLE hd03_tpcds.customer CASCADE;
TRUNCATE TABLE hd03_tpcds.customer_address CASCADE;
TRUNCATE TABLE hd03_tpcds.date_dim CASCADE;

INSERT INTO hd03_tpcds.pilot_metadata (benchmark, scale, data_dir, loaded_at)
VALUES ('tpcds', :'scale', :'data_dir', now())
ON CONFLICT (benchmark) DO UPDATE
SET scale = EXCLUDED.scale,
    data_dir = EXCLUDED.data_dir,
    loaded_at = EXCLUDED.loaded_at;

INSERT INTO hd03_tpcds.date_dim (d_date_sk, d_year, d_moy)
VALUES
  (1, 2001, 1),
  (2, 2001, 2),
  (3, 2001, 3)
ON CONFLICT (d_date_sk) DO UPDATE
SET d_year = EXCLUDED.d_year,
    d_moy = EXCLUDED.d_moy;

INSERT INTO hd03_tpcds.customer_address (ca_address_sk, ca_state)
VALUES
  (10, 'CA'),
  (20, 'WA')
ON CONFLICT (ca_address_sk) DO UPDATE
SET ca_state = EXCLUDED.ca_state;

INSERT INTO hd03_tpcds.customer (c_customer_sk, c_current_addr_sk)
VALUES
  (100, 10),
  (200, 20)
ON CONFLICT (c_customer_sk) DO UPDATE
SET c_current_addr_sk = EXCLUDED.c_current_addr_sk;

INSERT INTO hd03_tpcds.item (i_item_sk, i_item_id, i_category, i_class, i_current_price)
VALUES
  (1000, 'ITEM0001', 'Books', 'business', 25.00),
  (2000, 'ITEM0002', 'Electronics', 'portable', 62.50),
  (3000, 'ITEM0003', 'Home', 'decor', 90.00)
ON CONFLICT (i_item_sk) DO UPDATE
SET i_item_id = EXCLUDED.i_item_id,
    i_category = EXCLUDED.i_category,
    i_class = EXCLUDED.i_class,
    i_current_price = EXCLUDED.i_current_price;

INSERT INTO hd03_tpcds.store_sales (
  ss_ticket_number,
  ss_sold_date_sk,
  ss_item_sk,
  ss_customer_sk,
  ss_quantity,
  ss_sales_price,
  ss_net_paid
)
VALUES
  (1, 1, 1000, 100, 2, 25.00, 50.00),
  (2, 2, 2000, 200, 4, 62.50, 250.00),
  (3, 3, 3000, 100, 5, 90.00, 450.00),
  (4, 2, 1000, 200, 3, 25.00, 75.00)
ON CONFLICT (ss_ticket_number) DO UPDATE
SET ss_sold_date_sk = EXCLUDED.ss_sold_date_sk,
    ss_item_sk = EXCLUDED.ss_item_sk,
    ss_customer_sk = EXCLUDED.ss_customer_sk,
    ss_quantity = EXCLUDED.ss_quantity,
    ss_sales_price = EXCLUDED.ss_sales_price,
    ss_net_paid = EXCLUDED.ss_net_paid;

COMMIT;
