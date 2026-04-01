# HD-03 Local Vendor Staging

Do not commit third-party benchmark binaries or benchmark source drops into the repository.

This directory defines the local staging layout for private or manually downloaded HD-03 benchmark kits on the frozen reference machine.

Supported local provisioning paths:

- prebuilt binaries:
  - `tools/hd03/vendor/bin/dbgen`
  - `tools/hd03/vendor/bin/dsdgen`
- optional local source trees:
  - `tools/hd03/vendor/src/tpch-dbgen/`
  - `tools/hd03/vendor/src/tpcds-kit/`

Current local machine prerequisites already present:

- `gcc`
- `make`
- `tar`
- `perl`

This is enough for a minimal local build path once the private source trees are staged.

When prebuilt binaries are staged locally, bind them into the runtime location with:

```bash
python -m scripts.hd03_toolchain_bind
```

Or bind explicit absolute paths:

```bash
python -m scripts.hd03_toolchain_bind \
  --tpch-dbgen-bin /abs/path/to/dbgen \
  --tpcds-dsdgen-bin /abs/path/to/dsdgen
```

The runtime resolver checks `tools/hd03/bin/` first, then the staging locations above, then `PATH`.

Minimal local provisioning flow on this machine:

1. Stage private source trees or prebuilt binaries under `tools/hd03/vendor/`.
2. If source trees are staged, inspect or build with:

```bash
python -m scripts.cli hd03-toolchain-prepare --benchmark all
python -m scripts.cli hd03-toolchain-prepare --benchmark all --execute
```

3. Bind the resolved binaries into `tools/hd03/bin/`:

```bash
python -m scripts.hd03_toolchain_bind
```

4. Re-check HD-03 toolchain state:

```bash
python -m scripts.cli hd03-pilot-toolchain-check --config results/hd03/<run_id>.inputs.json
```
