# HD-03 Runtime Manifests

These files define the minimum executable runtime wiring for a future HD-03 pilot.

They do not execute a real pilot by themselves.

Current usage:

- `tpch.load.json`
- `tpcds.load.json`
- `tpch.pilot.json`
- `tpcds.pilot.json`

The manifests point to:

- a local driver SQL file under `sql/hd03/`
- additional required benchmark assets that must exist before a real run can execute

If the required assets are absent, the runner blocks and reports the missing files.
