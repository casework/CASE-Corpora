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

PYTHON3 ?= python3

top_srcdir := $(shell cd ../../.. ; pwd)

supplemental_graph := $(wildcard supplemental.*)

maybe_ground_truth_graph := $(wildcard ground-truth.*)

rdf_toolkit_jar := $(top_srcdir)/dependencies/CASE/dependencies/UCO/lib/rdf-toolkit.jar

all: \
  kb.ttl

.PHONY: \
  check-case_validate \
  check-pytest \
  format

kb.ttl: \
  dataset.ttl \
  generated-ground-truth-prov.ttl \
  generated-prov.ttl
	rm -f _$@ __$@
	source $(top_srcdir)/venv/bin/activate \
	  && rdfpipe \
	    --output-format turtle \
	    $(top_srcdir)/catalog/catalog.ttl \
	    $(top_srcdir)/catalog/shared.ttl \
	    dataset.ttl \
	    distribution.ttl \
	    $(supplemental_graph) \
	    $(maybe_ground_truth_graph) \
	    generated-*.ttl \
	    > __$@
	java -jar $(rdf_toolkit_jar) \
	  --inline-blank-nodes \
	  --source-format turtle \
	  --source __$@ \
	  --target-format turtle \
	  --target _$@
	rm __$@
	mv _$@ $@

check: \
  check-case_validate \
  check-pytest

check-case_validate: \
  $(top_srcdir)/taxonomy/devices/drafting.ttl \
  kb.ttl
	source $(top_srcdir)/venv/bin/activate \
	  && case_validate \
	    --inference rdfs \
	    --ontology-graph $(top_srcdir)/dependencies/dependencies.ttl \
	    --ontology-graph $(top_srcdir)/shapes/case-corpora.ttl \
	    --ontology-graph $(top_srcdir)/shapes/dcat.ttl \
	    --ontology-graph $(top_srcdir)/shapes/dcat-us.ttl \
	    --ontology-graph $(top_srcdir)/shapes/dct.ttl \
	    --ontology-graph $(top_srcdir)/taxonomy/devices/drafting.ttl \
	    kb.ttl

check-pytest: \
  kb.ttl
	test 0 -eq $$(find * -maxdepth 0 -name 'test_*.py' | wc -l) \
	  || ( \
	    source $(top_srcdir)/venv/bin/activate \
	      && pytest \
	        --log-level=DEBUG \
	  )

clean:
	@rm -f \
	  generated-*.ttl \
	  kb-all.ttl

generated-ground-truth-prov.ttl: \
  $(maybe_ground_truth_graph) \
  generated-prov.ttl
	#TODO - Write 'subtracter' script to distill generated prov from generated ground truth prov.
	touch $@

generated-prov.ttl: \
  $(top_srcdir)/.venv.done.log \
  $(top_srcdir)/catalog/catalog.ttl \
  $(top_srcdir)/catalog/shared.ttl \
  distribution.ttl \
  $(supplemental_graph)
	rm -f _$@ __$@
	source $(top_srcdir)/venv/bin/activate \
	  && case_prov_rdf \
	    --allow-empty-results \
	    __$@ \
	    $(top_srcdir)/catalog/shared.ttl \
	    distribution.ttl \
	    $(supplemental_graph)
	java -jar $(rdf_toolkit_jar) \
	  --inline-blank-nodes \
	  --source-format turtle \
	  --source __$@ \
	  --target-format turtle \
	  --target _$@
	rm __$@
	mv _$@ $@
