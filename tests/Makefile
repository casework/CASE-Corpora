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

top_srcdir := $(shell cd .. ; pwd)

rdf_toolkit_jar := $(top_srcdir)/dependencies/CASE/dependencies/UCO/lib/rdf-toolkit.jar

validation_files := \
  distribution_PASS_validation.ttl \
  distribution_XFAIL_validation.ttl \
  owl_abox_XFAIL_inferencing_none_validation.ttl \
  owl_abox_XFAIL_inferencing_owlrl_validation.ttl \
  owl_abox_XFAIL_inferencing_rdfs_validation.ttl

all: \
  $(validation_files)

check: \
  $(validation_files)
	source $(top_srcdir)/venv/bin/activate \
	  && pytest

clean:
	@rm -f \
	  $(validation_files)

distribution_PASS_validation.ttl: \
  $(top_srcdir)/.venv.done.log \
  $(top_srcdir)/dependencies/dependencies.ttl \
  $(top_srcdir)/ontology/case-corpora.ttl \
  $(top_srcdir)/shapes/local.ttl \
  $(top_srcdir)/shapes/shapes.ttl \
  distribution_PASS.ttl
	rm -f __$@ _$@
	source $(top_srcdir)/venv/bin/activate \
	  && case_validate \
	    --allow-infos \
	    --format turtle \
	    --inference rdfs \
	    --ontology-graph $(top_srcdir)/dependencies/dependencies.ttl \
	    --ontology-graph $(top_srcdir)/ontology/case-corpora.ttl \
	    --ontology-graph $(top_srcdir)/shapes/local.ttl \
	    --ontology-graph $(top_srcdir)/shapes/shapes.ttl \
	    --output __$@ \
	    distribution_PASS.ttl
	java -jar $(rdf_toolkit_jar) \
	  --inline-blank-nodes \
	  --source-format turtle \
	  --source __$@ \
	  --target-format turtle \
	  --target _$@
	rm __$@
	mv _$@ $@

distribution_XFAIL_validation.ttl: \
  $(top_srcdir)/.venv.done.log \
  $(top_srcdir)/dependencies/dependencies.ttl \
  $(top_srcdir)/ontology/case-corpora.ttl \
  $(top_srcdir)/shapes/local.ttl \
  $(top_srcdir)/shapes/shapes.ttl \
  distribution_XFAIL.ttl
	rm -f __$@ _$@
	source $(top_srcdir)/venv/bin/activate \
	  && case_validate \
	    --allow-infos \
	    --format turtle \
	    --inference rdfs \
	    --ontology-graph $(top_srcdir)/dependencies/dependencies.ttl \
	    --ontology-graph $(top_srcdir)/ontology/case-corpora.ttl \
	    --ontology-graph $(top_srcdir)/shapes/local.ttl \
	    --ontology-graph $(top_srcdir)/shapes/shapes.ttl \
	    --output __$@ \
	    distribution_XFAIL.ttl \
	    ; rc=$$? ; test 1 -eq $$rc
	java -jar $(rdf_toolkit_jar) \
	  --inline-blank-nodes \
	  --source-format turtle \
	  --source __$@ \
	  --target-format turtle \
	  --target _$@
	rm __$@
	mv _$@ $@

owl_abox_XFAIL_inferencing_none_validation.ttl: \
  $(top_srcdir)/.venv.done.log \
  $(top_srcdir)/shapes/sh-owl-abox.ttl \
  owl_abox_XFAIL.ttl
	rm -f __$@ _$@
	source $(top_srcdir)/venv/bin/activate \
	  && pyshacl \
	    --format turtle \
	    --metashacl \
	    --output __$@ \
	    --shacl $(top_srcdir)/shapes/sh-owl-abox.ttl \
	    owl_abox_XFAIL.ttl \
	    ; rc=$$? ; test 1 -eq $$rc
	java -jar $(rdf_toolkit_jar) \
	  --inline-blank-nodes \
	  --source-format turtle \
	  --source __$@ \
	  --target-format turtle \
	  --target _$@
	rm __$@
	mv _$@ $@

owl_abox_XFAIL_inferencing_owlrl_validation.ttl: \
  $(top_srcdir)/.venv.done.log \
  $(top_srcdir)/shapes/sh-owl-abox.ttl \
  owl_abox_XFAIL.ttl
	rm -f __$@ _$@
	source $(top_srcdir)/venv/bin/activate \
	  && pyshacl \
	    --format turtle \
	    --inference owlrl \
	    --metashacl \
	    --output __$@ \
	    --shacl $(top_srcdir)/shapes/sh-owl-abox.ttl \
	    owl_abox_XFAIL.ttl \
	    ; rc=$$? ; test 1 -eq $$rc
	java -jar $(rdf_toolkit_jar) \
	  --inline-blank-nodes \
	  --source-format turtle \
	  --source __$@ \
	  --target-format turtle \
	  --target _$@
	rm __$@
	mv _$@ $@

owl_abox_XFAIL_inferencing_rdfs_validation.ttl: \
  $(top_srcdir)/.venv.done.log \
  $(top_srcdir)/shapes/sh-owl-abox.ttl \
  owl_abox_XFAIL.ttl
	rm -f __$@ _$@
	source $(top_srcdir)/venv/bin/activate \
	  && pyshacl \
	    --format turtle \
	    --inference rdfs \
	    --metashacl \
	    --output __$@ \
	    --shacl $(top_srcdir)/shapes/sh-owl-abox.ttl \
	    owl_abox_XFAIL.ttl \
	    ; rc=$$? ; test 1 -eq $$rc
	java -jar $(rdf_toolkit_jar) \
	  --inline-blank-nodes \
	  --source-format turtle \
	  --source __$@ \
	  --target-format turtle \
	  --target _$@
	rm __$@
	mv _$@ $@
