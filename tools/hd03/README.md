# HD-03 Toolchain Binding

This directory is the local binding target for benchmark-generator binaries used by HD-03.

Expected bound paths:

- `tools/hd03/bin/dbgen`
- `tools/hd03/bin/dsdgen`

These paths may be created by:

```bash
python -m scripts.hd03_toolchain_bind --tpch-dbgen-bin /abs/path/to/dbgen --tpcds-dsdgen-bin /abs/path/to/dsdgen
```

If the binaries are already staged under `tools/hd03/vendor/bin/`, run:

```bash
python -m scripts.hd03_toolchain_bind
```

If the binaries are not bound here and are not available on `PATH`, HD-03 cannot run a real benchmark pilot.

Minimal smoke-level SQL assets live under:

- `sql/hd03/assets/tpch/`
- `sql/hd03/assets/tpcds/`
