\set ON_ERROR_STOP on

-- Minimal executable TPCDS smoke schema for HD-03 wiring checks.
-- Replace with benchmark-faithful assets when the real TPCDS kit is provisioned.

CREATE SCHEMA IF NOT EXISTS hd03_tpcds;

CREATE TABLE IF NOT EXISTS hd03_tpcds.pilot_metadata (
  benchmark text PRIMARY KEY,
  scale text NOT NULL,
  data_dir text NOT NULL,
  loaded_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS hd03_tpcds.store_sales_smoke (
  sold_date_sk integer PRIMARY KEY,
  item_sk integer NOT NULL,
  customer_sk integer NOT NULL,
  net_paid numeric(15, 2) NOT NULL,
  quantity integer NOT NULL,
  sales_price numeric(15, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS hd03_tpcds.date_dim_smoke (
  d_date_sk integer PRIMARY KEY,
  d_year integer NOT NULL,
  d_moy integer NOT NULL
);
