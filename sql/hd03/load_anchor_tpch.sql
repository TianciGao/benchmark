\set ON_ERROR_STOP on

-- Minimal executable TPC-H load driver for HD-03 pilot-smoke wiring.
-- This is not the official TPC-H schema or data-loading pipeline.

\if :{?data_dir}
\else
  \echo 'hd03_load_anchor_tpch.sql requires psql variable data_dir'
  \quit 3
\endif

\if :{?scale}
\else
  \echo 'hd03_load_anchor_tpch.sql requires psql variable scale'
  \quit 3
\endif

\ir assets/tpch/schema.sql
\ir assets/tpch/load.sql
