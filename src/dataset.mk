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

# Usage context:
# This is expected to run in directories following this pattern:
# $(top_srcdir)/catalog/datasets/$(dataset)/
#
# This file is assumed to be used with a Make 'include' directive.
#
# The Make variable extra_supplement_graphs, if to be used, should be
# defined before the 'include' directive.

SHELL := /bin/bash

PYTHON3 ?= python3

top_srcdir := $(shell cd ../../.. ; pwd)

supplemental_graph := $(wildcard supplemental.*)

maybe_ground_truth_graph := $(wildcard ground-truth.*)

rdf_toolkit_jar := $(top_srcdir)/dependencies/CASE/dependencies/UCO/lib/rdf-toolkit.jar

all: \
  kb.ttl

%.png: \
  %.dot
	dot \
	  -T png \
	  -o _$@ \
	  $<
	mv _$@ $@

%.svg: \
  %.dot
	dot \
	  -T svg \
	  -o _$@ \
	  $<
	mv _$@ $@

.PHONY: \
  check-case_prov_check \
  check-pytest \
  figures

# TODO - This supplementary file can be removed after adding an --inference flag to case_prov_rdf similar in function to the same flag on case_validate.
base_rdfs_expansion.ttl: \
  $(top_srcdir)/.venv.done.log \
  $(top_srcdir)/ontology/case-corpora.ttl \
  $(top_srcdir)/src/rdfs_expansion_ttl.py \
  dataset.ttl \
  distribution.ttl \
  $(extra_supplement_graphs) \
  $(supplemental_graph)
	source $(top_srcdir)/venv/bin/activate \
	  && python3 $(top_srcdir)/src/rdfs_expansion_ttl.py \
	    _$@ \
	    $(top_srcdir)/ontology/case-corpora.ttl \
	    dataset.ttl \
	    distribution.ttl \
	    $(extra_supplement_graphs) \
	    $(supplemental_graph)
	mv _$@ $@

# Review order is:
# 1. Is the CASE graph conformat?  (Necessary for kb.ttl to build.)
# 2. Does the overall PROV-O graph (hand-coded and generated) having any errors?
# 3. Do review tests written in Python pass?
check: \
  check-case_prov_check \
  check-pytest

check-case_prov_check: \
  kb.ttl
	source $(top_srcdir)/venv/bin/activate \
	  && case_prov_check \
	    --allow-warnings \
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
	  *.dot \
	  *.png \
	  *.svg \
	  generated-*.ttl \
	  kb.ttl \
	  kb_validation-*.ttl

figures: \
  generated-prov.png \
  generated-prov.svg

generated-ground-truth-prov.ttl: \
  $(maybe_ground_truth_graph) \
  generated-prov.ttl
	#TODO - Write 'subtracter' script to distill generated prov from generated ground truth prov.
	touch $@

generated-prov.dot: \
  generated-prov.ttl
	source $(top_srcdir)/venv/bin/activate \
	  && case_prov_dot \
	    --dash-unqualified \
	    _$@ \
	    generated-prov.ttl \
	    supplemental.ttl
	mv _$@ $@

generated-prov.ttl: \
  $(top_srcdir)/.venv.done.log \
  $(top_srcdir)/catalog/catalog.ttl \
  $(top_srcdir)/catalog/shared.ttl \
  base_rdfs_expansion.ttl
	rm -f _$@ __$@
	source $(top_srcdir)/venv/bin/activate \
	  && case_prov_rdf \
	    --allow-empty-results \
	    __$@ \
	    $(top_srcdir)/catalog/shared.ttl \
	    base_rdfs_expansion.ttl \
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

kb.ttl: \
  $(top_srcdir)/dependencies/dependencies.ttl \
  $(top_srcdir)/ontology/case-corpora.ttl \
  $(top_srcdir)/shapes/local.ttl \
  $(top_srcdir)/shapes/shapes.ttl \
  $(top_srcdir)/taxonomy/devices/drafting.ttl \
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
	# Skip per-dataset validation when this file is called in a GitHub action.
	test ! -z "$${GITHUB_ACTIONS+x}" \
	  || ( \
	    source $(top_srcdir)/venv/bin/activate \
	      && case_validate \
	        --allow-infos \
	        --inference rdfs \
	        --ontology-graph $(top_srcdir)/dependencies/dependencies.ttl \
	        --ontology-graph $(top_srcdir)/ontology/case-corpora.ttl \
	        --ontology-graph $(top_srcdir)/shapes/local.ttl \
	        --ontology-graph $(top_srcdir)/shapes/shapes.ttl \
	        --ontology-graph $(top_srcdir)/taxonomy/devices/drafting.ttl \
	        __$@ \
	    )
	java -jar $(rdf_toolkit_jar) \
	  --inline-blank-nodes \
	  --source-format turtle \
	  --source __$@ \
	  --target-format turtle \
	  --target _$@
	rm __$@
	mv _$@ $@
