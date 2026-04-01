\set ON_ERROR_STOP on

-- Minimal executable TPCH smoke schema for HD-03 wiring checks.
-- Replace with benchmark-faithful assets when the real TPCH kit is provisioned.

CREATE SCHEMA IF NOT EXISTS hd03_tpch;

CREATE TABLE IF NOT EXISTS hd03_tpch.pilot_metadata (
  benchmark text PRIMARY KEY,
  scale text NOT NULL,
  data_dir text NOT NULL,
  loaded_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS hd03_tpch.lineitem_smoke (
  orderkey bigint PRIMARY KEY,
  partkey bigint NOT NULL,
  suppkey bigint NOT NULL,
  quantity numeric(15, 2) NOT NULL,
  extendedprice numeric(15, 2) NOT NULL,
  discount numeric(5, 2) NOT NULL,
  tax numeric(5, 2) NOT NULL,
  returnflag text NOT NULL,
  linestatus text NOT NULL,
  shipdate date NOT NULL
);

CREATE TABLE IF NOT EXISTS hd03_tpch.orders_smoke (
  orderkey bigint PRIMARY KEY,
  custkey bigint NOT NULL,
  orderstatus text NOT NULL,
  totalprice numeric(15, 2) NOT NULL,
  orderdate date NOT NULL,
  orderpriority text NOT NULL,
  clerk text NOT NULL
);
