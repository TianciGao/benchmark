PYTHON ?= python

.PHONY: setup smoke pack-freeze eval-raw eval-deploy verify-cases tables figures postgres-env-check artifact-preflight hd03-pilot-init hd03-pilot-check-inputs

setup:
	$(PYTHON) -m scripts.cli setup

smoke:
	$(PYTHON) -m scripts.cli smoke

pack-freeze:
	$(PYTHON) -m scripts.cli pack-freeze

eval-raw:
	$(PYTHON) -m scripts.cli eval-raw

eval-deploy:
	$(PYTHON) -m scripts.cli eval-deploy

verify-cases:
	$(PYTHON) -m scripts.cli verify-cases

tables:
	$(PYTHON) -m scripts.cli tables

figures:
	$(PYTHON) -m scripts.cli figures

postgres-env-check:
	$(PYTHON) -m scripts.cli postgres-env-check

artifact-preflight:
	$(PYTHON) -m scripts.cli artifact-preflight

hd03-pilot-init:
	$(PYTHON) -m scripts.cli hd03-pilot-init

hd03-pilot-check-inputs:
	$(PYTHON) -m scripts.cli hd03-pilot-check-inputs --config $(CONFIG)
