#!/usr/bin/make -f

# This software was developed at the National Institute of Standards
# and Technology by employees of the Federal Government in the course
# of their official duties. Pursuant to title 17 Section 105 of the
# United States Code this software is not subject to copyright
# protection and is in the public domain. NIST assumes no
# responsibility whatsoever for its use by other parties, and makes
# no guarantees, expressed or implied, about its quality,
# reliability, or any other characteristic.
#
# We would appreciate acknowledgement if the software is used.

SHELL := /bin/bash

all: \
  .venv-pre-commit/var/.pre-commit-built.log \
  all-shapes \
  all-var
	$(MAKE) \
	  --directory catalog
	$(MAKE) \
	  --directory reports

.PHONY: \
  all-dependencies \
  all-ontology \
  all-shapes \
  all-taxonomy \
  all-tests \
  all-var \
  check-catalog \
  check-dependencies \
  check-mypy \
  check-ontology \
  check-reports \
  check-shapes \
  check-supply-chain \
  check-supply-chain-pre-commit \
  check-taxonomy \
  check-tests

.git_submodule_init.done.log: \
  .gitmodules
	# CASE (to retrieve rdf-toolkit)
	test -r dependencies/CASE/README.md \
	  || git submodule update \
	    --init \
	    dependencies/CASE
	# CASE-develop
	test -r dependencies/CASE-develop/README.md \
	  || git submodule update \
	    --init \
	    dependencies/CASE-develop
	$(MAKE) \
	  --directory dependencies/CASE-develop \
	  .git_submodule_init.done.log
	# CASE-unstable
	test -r dependencies/CASE-unstable/README.md \
	  || git submodule update \
	    --init \
	    dependencies/CASE-unstable
	$(MAKE) \
	  --directory dependencies/CASE-unstable \
	  .git_submodule_init.done.log
	# cito
	test -r dependencies/cito/README.md \
	  || git submodule update \
	    --init \
	    dependencies/cito
	# sdw
	test -r dependencies/sdw/README.md \
	  || git submodule update \
	    --init \
	    dependencies/sdw
	# swan-ontology
	test -r dependencies/swan-ontology/README.md \
	  || git submodule update \
	    --init \
	    dependencies/swan-ontology
	$(MAKE) \
	  --directory dependencies/CASE \
	  .lib.done.log
	touch $@

.venv.done.log: \
  dependencies/CASE/dependencies/UCO/dependencies/CASE-Utility-SHACL-Inheritance-Reviewer/case_shacl_inheritance_reviewer/__init__.py \
  dependencies/CASE/dependencies/UCO/dependencies/CASE-Utility-SHACL-Inheritance-Reviewer/setup.cfg \
  dependencies/CASE/dependencies/UCO/tests/requirements.txt \
  requirements.txt
	python3 -m venv \
	  venv
	source venv/bin/activate \
	  && pip install \
	    --upgrade \
	    pip \
	    setuptools \
	    wheel
	source venv/bin/activate \
	  && pip install \
	    --requirement requirements.txt
	source venv/bin/activate \
	  && pip install \
	    dependencies/CASE/dependencies/UCO/dependencies/CASE-Utility-SHACL-Inheritance-Reviewer
	source venv/bin/activate \
	  && pip install \
	    --requirement dependencies/CASE/dependencies/UCO/tests/requirements.txt
	touch $@

# This virtual environment is meant to be built once and then persist, even through 'make clean'.
# If a recipe is written to remove this flag file, it should first run `pre-commit uninstall`.
.venv-pre-commit/var/.pre-commit-built.log:
	rm -rf .venv-pre-commit
	test -r .pre-commit-config.yaml \
	  || (echo "ERROR:Makefile:pre-commit is expected to install for this repository, but .pre-commit-config.yaml does not seem to exist." >&2 ; exit 1)
	python3 -m venv \
	  .venv-pre-commit
	source .venv-pre-commit/bin/activate \
	  && pip install \
	    --upgrade \
	    pip \
	    setuptools \
	    wheel
	source .venv-pre-commit/bin/activate \
	  && pip install \
	    pre-commit
	source .venv-pre-commit/bin/activate \
	  && pre-commit install
	mkdir -p \
	  .venv-pre-commit/var
	touch $@

all-dependencies: \
  .venv.done.log
	$(MAKE) \
	  --directory dependencies

all-ontology: \
  all-dependencies
	$(MAKE) \
	  --directory ontology

all-shapes: \
  all-ontology
	$(MAKE) \
	  --directory shapes

all-taxonomy: \
  all-dependencies
	$(MAKE) \
	  --directory taxonomy/devices

all-tests: \
  all-shapes
	$(MAKE) \
	  --directory tests

# This descent recipe balances resource local availability, resource
# remote availability, and Git noise from resource regeneration.
#
# If the remote resource (Digital Corpora's index.tsv) becomes
# unavailable or alters its format, GitHub CI will continue to work for
# CASE-Corpora on runs unrelated to updating Digital Corpora references.
# If a developer runs a local build, the TSV resoure will be refreshed
# and can be reviewed and committed independently.
# Record churn from Digital Corpora's scan updates (particularly record
# mtimes) will not cause significant Git noise for CASE-Corpora, because
# the 'var/' folder filters the Git-tracked records to those listed as
# used under 'catalog/datasets/digitalcorpora-*'.
#
# An extra reset-retry step is added on the descending Make call to
# handle the case where new Digital Corpora references are committed
# under 'catalog/', but not committed to the Git-tracked TSV under
# 'var/'.  Without this retry step, CI fails for a reason not relevant
# to the maintainer's local development environment.  This case does
# trigger a CI download from Digital Corpora, but the download will only
# apply until the TSV update is committed.
all-var:
	test "x$${GITHUB_ACTIONS}" != "xtrue" \
	  || cp \
	    -n \
	    -v \
	    var/digital_corpora_index.tsv \
	    var/cached-digital_corpora_index.tsv \
	    || test -r \
	      var/cached-digital_corpora_index.tsv
	$(MAKE) \
	  --directory var \
	  || ( \
	    $(MAKE) \
	      --directory var \
	      clean \
	      && $(MAKE) \
	        --directory var \
	  )

check: \
  .venv-pre-commit/var/.pre-commit-built.log \
  check-mypy \
  check-reports \
  check-tests

check-catalog: \
  all-var \
  check-shapes \
  check-taxonomy
	$(MAKE) \
	  --directory catalog \
	  check

check-dependencies: \
  all-dependencies
	$(MAKE) \
	  --directory dependencies \
	  check

check-mypy: \
  .venv.done.log
	source venv/bin/activate \
	  && mypy --strict \
	    catalog \
	    src \
	    tests

check-ontology: \
  all-ontology \
  check-dependencies
	$(MAKE) \
	  --directory ontology \
	  check

check-reports: \
  check-catalog
	$(MAKE) \
	  --directory reports \
	  check

check-shapes: \
  all-shapes \
  check-ontology
	$(MAKE) \
	  --directory shapes \
	  check

check-supply-chain: \
  check-supply-chain-pre-commit

check-supply-chain-pre-commit: \
  .venv-pre-commit/var/.pre-commit-built.log
	source .venv-pre-commit/bin/activate \
	  && pre-commit autoupdate
	git diff \
	  --exit-code \
	  .pre-commit-config.yaml

check-taxonomy: \
  all-taxonomy \
  check-shapes
	$(MAKE) \
	  --directory taxonomy/devices \
	  check

check-tests: \
  all-tests \
  check-shapes
	$(MAKE) \
	  --directory tests \
	  check

clean:
	@$(MAKE) \
	  --directory reports \
	  clean
	@$(MAKE) \
	  --directory taxonomy/devices \
	  clean
	@$(MAKE) \
	  --directory shapes \
	  clean
	@$(MAKE) \
	  --directory ontology \
	  clean
	@$(MAKE) \
	  --directory catalog \
	  clean
	@$(MAKE) \
	  --directory dependencies \
	  clean
	@$(MAKE) \
	  --directory var \
	  clean
	@rm -f \
	  .*.done.log

dependencies/CASE/dependencies/UCO/dependencies/CASE-Utility-SHACL-Inheritance-Reviewer/case_shacl_inheritance_reviewer/__init__.py: \
  .git_submodule_init.done.log
	test -r $@
	touch $@

dependencies/CASE/dependencies/UCO/dependencies/CASE-Utility-SHACL-Inheritance-Reviewer/setup.cfg: \
  .git_submodule_init.done.log
	test -r $@
	touch $@

dependencies/CASE/dependencies/UCO/tests/requirements.txt: \
  .git_submodule_init.done.log
	test -r $@
	touch $@
