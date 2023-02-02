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
  all-shapes
	$(MAKE) \
	  --directory catalog
	$(MAKE) \
	  --directory reports

.PHONY: \
  all-dependencies \
  all-shapes \
  all-taxonomy \
  all-tests \
  check-catalog \
  check-dependencies \
  check-ontology \
  check-reports \
  check-shapes \
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
	# CASE-unstable
	test -r dependencies/CASE-unstable/README.md \
	  || git submodule update \
	    --init \
	    dependencies/CASE-unstable
	$(MAKE) \
	  --directory dependencies/CASE-unstable \
	  .git_submodule_init.done.log
	# UCO-develop
	test -r dependencies/UCO-develop/README.md \
	  || git submodule update \
	    --init \
	    dependencies/UCO-develop
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

all-shapes: \
  all-dependencies
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

check: \
  .venv-pre-commit/var/.pre-commit-built.log \
  check-reports \
  check-tests

check-catalog: \
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

check-ontology: \
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
