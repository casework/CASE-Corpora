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
  all-shapes

all-dependencies: \
  .venv.done.log
	$(MAKE) \
	  --directory dependencies

all-shapes: \
  all-dependencies
	$(MAKE) \
	  --directory shapes

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
	# UCO-develop
	test -r dependencies/UCO-develop/README.md \
	  || git submodule update \
	    --init \
	    dependencies/UCO-develop
	# UCO-unstable
	test -r dependencies/UCO-unstable/README.md \
	  || git submodule update \
	    --init \
	    dependencies/UCO-unstable
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

check: \
  .venv-pre-commit/var/.pre-commit-built.log \
  all-shapes
	$(MAKE) \
	  --directory ontology \
	  check
	$(MAKE) \
	  --directory shapes \
	  check
	$(MAKE) \
	  --directory catalog \
	  check
	$(MAKE) \
	  --directory reports \
	  check

clean:
	@$(MAKE) \
	  --directory reports \
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
