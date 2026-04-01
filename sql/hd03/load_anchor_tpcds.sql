\set ON_ERROR_STOP on

-- Minimal executable TPC-DS load driver for HD-03 pilot-smoke wiring.
-- This is not the official TPC-DS schema or data-loading pipeline.

\if :{?data_dir}
\else
  \echo 'hd03_load_anchor_tpcds.sql requires psql variable data_dir'
  \quit 3
\endif

\if :{?scale}
\else
  \echo 'hd03_load_anchor_tpcds.sql requires psql variable scale'
  \quit 3
\endif

\ir assets/tpcds/schema.sql
\ir assets/tpcds/load.sql
