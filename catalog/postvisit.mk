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

# This file is intended to be run after a recursive Make call is done
# within the datasets directory.  Some files needed by Make listing
# variables aren't guaranteed to exist before that descent.

SHELL := /bin/bash

top_srcdir := $(shell cd .. ; pwd)

rdf_toolkit_jar := $(top_srcdir)/dependencies/CASE/dependencies/UCO/lib/rdf-toolkit.jar

# Dataset and distribution files are aggregated together so datasets will have at least one distribution at minimal-requirements validation time.
kb_datasets_dependencies := \
  catalog.ttl \
  shared.ttl \
  $(wildcard datasets/*/dataset.ttl) \
  $(wildcard datasets/*/distribution.ttl)

kb_all_dependencies := \
  kb-datasets.ttl \
  $(top_srcdir)/taxonomy/devices/drafting.ttl \
  $(wildcard datasets/*/generated-*.ttl) \
  $(wildcard datasets/*/supplemental.ttl)

all: \
  README.md \
  kb-all.ttl

README.md: \
  README.md.in \
  README.md.sed \
  datasets.md
	sed \
	  -f README.md.sed \
	  README.md.in \
	  > _$@
	mv _$@ $@

check: \
  validate-kb-all.ttl

datasets.md: \
  $(top_srcdir)/shapes/shapes.ttl \
  datasets.sparql \
  kb-all.ttl
	source $(top_srcdir)/venv/bin/activate \
	  && case_sparql_select \
	    _$@ \
	    datasets.sparql \
	    $(top_srcdir)/shapes/shapes.ttl \
	    kb-all.ttl
	mv _$@ $@

kb-all.ttl: \
  $(kb_all_dependencies) \
  $(rdf_toolkit_jar) \
  $(top_srcdir)/.venv.done.log
	rm -f __$@ _$@
	source $(top_srcdir)/venv/bin/activate \
	  && rdfpipe \
	    --output-format turtle \
	    $(kb_all_dependencies) \
	    > __$@
	java -jar $(rdf_toolkit_jar) \
	  --inline-blank-nodes \
	  --source-format turtle \
	  --source __$@ \
	  --target-format turtle \
	  --target _$@
	rm __$@
	mv _$@ $@

kb-datasets.ttl: \
  $(kb_datasets_dependencies) \
  $(rdf_toolkit_jar) \
  $(top_srcdir)/.venv.done.log
	rm -f __$@ _$@
	source $(top_srcdir)/venv/bin/activate \
	  && rdfpipe \
	    --output-format turtle \
	    $(kb_datasets_dependencies) \
	    > __$@
	java -jar $(rdf_toolkit_jar) \
	  --inline-blank-nodes \
	  --source-format turtle \
	  --source __$@ \
	  --target-format turtle \
	  --target _$@
	rm __$@
	mv _$@ $@

validate-kb-all.ttl: \
  kb-all.ttl \
  validate-kb-datasets.ttl
	rm -f _$@
	source $(top_srcdir)/venv/bin/activate \
	  && case_validate \
	    --allow-infos \
	    --format turtle \
	    --inference rdfs \
	    --ontology-graph $(top_srcdir)/dependencies/dependencies.ttl \
	    --ontology-graph $(top_srcdir)/shapes/debug.ttl \
	    --ontology-graph $(top_srcdir)/shapes/shapes.ttl \
	    --output _$@ \
	    kb-all.ttl \
	    || (cat _$@ ; exit 1)
	mv _$@ $@

validate-kb-datasets.ttl: \
  kb-datasets.ttl \
  validate-catalog.ttl
	rm -f _$@
	source $(top_srcdir)/venv/bin/activate \
	  && case_validate \
	    --allow-infos \
	    --format turtle \
	    --inference rdfs \
	    --ontology-graph $(top_srcdir)/dependencies/dependencies.ttl \
	    --ontology-graph $(top_srcdir)/shapes/debug.ttl \
	    --ontology-graph $(top_srcdir)/shapes/shapes.ttl \
	    --output _$@ \
	    kb-datasets.ttl \
	    || (cat _$@ ; exit 1)
	mv _$@ $@
