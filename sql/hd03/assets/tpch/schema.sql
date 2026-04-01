\set ON_ERROR_STOP on

-- Benchmark-shaped minimal TPCH pilot schema for HD-03.
-- This is not a full TPC-H kit export, but the table names and joins are aligned
-- with the pilot queries Q9, Q18, and Q21 so a later real pilot smoke can swap in
-- benchmark-faithful generated data with the same runtime entry points.

CREATE SCHEMA IF NOT EXISTS hd03_tpch;

CREATE TABLE IF NOT EXISTS hd03_tpch.pilot_metadata (
  benchmark text PRIMARY KEY,
  scale text NOT NULL,
  data_dir text NOT NULL,
  loaded_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS hd03_tpch.nation (
  n_nationkey integer PRIMARY KEY,
  n_name text NOT NULL
);

CREATE TABLE IF NOT EXISTS hd03_tpch.supplier (
  s_suppkey integer PRIMARY KEY,
  s_name text NOT NULL,
  s_nationkey integer NOT NULL REFERENCES hd03_tpch.nation (n_nationkey)
);

CREATE TABLE IF NOT EXISTS hd03_tpch.part (
  p_partkey integer PRIMARY KEY,
  p_name text NOT NULL
);

CREATE TABLE IF NOT EXISTS hd03_tpch.partsupp (
  ps_partkey integer NOT NULL REFERENCES hd03_tpch.part (p_partkey),
  ps_suppkey integer NOT NULL REFERENCES hd03_tpch.supplier (s_suppkey),
  ps_supplycost numeric(15, 2) NOT NULL,
  PRIMARY KEY (ps_partkey, ps_suppkey)
);

CREATE TABLE IF NOT EXISTS hd03_tpch.customer (
  c_custkey integer PRIMARY KEY,
  c_name text NOT NULL
);

CREATE TABLE IF NOT EXISTS hd03_tpch.orders (
  o_orderkey integer PRIMARY KEY,
  o_custkey integer NOT NULL REFERENCES hd03_tpch.customer (c_custkey),
  o_orderstatus text NOT NULL,
  o_totalprice numeric(15, 2) NOT NULL,
  o_orderdate date NOT NULL,
  o_orderpriority text NOT NULL
);

CREATE TABLE IF NOT EXISTS hd03_tpch.lineitem (
  l_orderkey integer NOT NULL REFERENCES hd03_tpch.orders (o_orderkey),
  l_partkey integer NOT NULL REFERENCES hd03_tpch.part (p_partkey),
  l_suppkey integer NOT NULL REFERENCES hd03_tpch.supplier (s_suppkey),
  l_linenumber integer NOT NULL,
  l_quantity numeric(15, 2) NOT NULL,
  l_extendedprice numeric(15, 2) NOT NULL,
  l_discount numeric(5, 2) NOT NULL,
  l_returnflag text NOT NULL,
  l_linestatus text NOT NULL,
  l_shipdate date NOT NULL,
  l_receiptdate date NOT NULL,
  l_commitdate date NOT NULL,
  PRIMARY KEY (l_orderkey, l_linenumber)
);
