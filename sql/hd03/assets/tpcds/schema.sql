\set ON_ERROR_STOP on

-- Benchmark-shaped minimal TPCDS pilot schema for HD-03.
-- This is not a full TPC-DS kit export, but the table names and joins are aligned
-- with the pilot queries Q64, Q72, and Q95 so a later real pilot smoke can swap in
-- benchmark-faithful generated data with the same runtime entry points.

CREATE SCHEMA IF NOT EXISTS hd03_tpcds;

CREATE TABLE IF NOT EXISTS hd03_tpcds.pilot_metadata (
  benchmark text PRIMARY KEY,
  scale text NOT NULL,
  data_dir text NOT NULL,
  loaded_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS hd03_tpcds.date_dim (
  d_date_sk integer PRIMARY KEY,
  d_year integer NOT NULL,
  d_moy integer NOT NULL
);

CREATE TABLE IF NOT EXISTS hd03_tpcds.customer_address (
  ca_address_sk integer PRIMARY KEY,
  ca_state text NOT NULL
);

CREATE TABLE IF NOT EXISTS hd03_tpcds.customer (
  c_customer_sk integer PRIMARY KEY,
  c_current_addr_sk integer NOT NULL REFERENCES hd03_tpcds.customer_address (ca_address_sk)
);

CREATE TABLE IF NOT EXISTS hd03_tpcds.item (
  i_item_sk integer PRIMARY KEY,
  i_item_id text NOT NULL,
  i_category text NOT NULL,
  i_class text NOT NULL,
  i_current_price numeric(15, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS hd03_tpcds.store_sales (
  ss_ticket_number integer PRIMARY KEY,
  ss_sold_date_sk integer NOT NULL REFERENCES hd03_tpcds.date_dim (d_date_sk),
  ss_item_sk integer NOT NULL REFERENCES hd03_tpcds.item (i_item_sk),
  ss_customer_sk integer NOT NULL REFERENCES hd03_tpcds.customer (c_customer_sk),
  ss_quantity integer NOT NULL,
  ss_sales_price numeric(15, 2) NOT NULL,
  ss_net_paid numeric(15, 2) NOT NULL
);
