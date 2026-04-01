# HD-03 TPCDS Pilot Assets

These files are benchmark-shaped pilot assets for `HD-03`.

They are intentionally minimal:

- table names and join structure are aligned with TPCDS pilot queries `Q64`, `Q72`, and `Q95`
- the data volume is tiny and only supports smoke execution
- the files are designed so a later local `dsdgen`-based load path can replace the seed rows without changing the runtime driver paths

They are not a frozen scale decision and not a full benchmark dataset.
