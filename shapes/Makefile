#!/usr/bin/make -f

# Portions of this file contributed by NIST are governed by the
# following statement:
#
# This software was developed at the National Institute of Standards
# and Technology by employees of the Federal Government in the course
# of their official duties. Pursuant to Title 17 Section 105 of the
# United States Code, this software is not subject to copyright
# protection within the United States. NIST assumes no responsibility
# whatsoever for its use by other parties, and makes no guarantees,
# expressed or implied, about its quality, reliability, or any other
# characteristic.
#
# We would appreciate acknowledgement if the software is used.

SHELL := /bin/bash

top_srcdir := $(shell cd .. ; pwd)

case_srcdir := $(top_srcdir)/dependencies/CASE

uco_srcdir := $(case_srcdir)/dependencies/UCO

shapes_ttl_sources := $(wildcard sh-*.ttl)
shape_files := \
  $(shapes_ttl_sources) \
  local.ttl
check_shape_files := $(foreach shape_file,$(shape_files),.check-$(shape_file))
check_shape_targets := $(foreach shape_file,$(shape_files),check-$(shape_file))

all: \
  catalog-v001.xml \
  shapes.ttl

.PRECIOUS: \
  .check-%.ttl

.check-%.ttl: \
  %.ttl
	java -jar $(top_srcdir)/dependencies/CASE/dependencies/UCO/lib/rdf-toolkit.jar \
	  --inline-blank-nodes \
	  --source $< \
	  --source-format turtle \
	  --target _$@ \
	  --target-format turtle
	mv _$@ $@

catalog-v001.xml: \
  $(case_srcdir)/ontology/master/catalog-v001.xml \
  $(top_srcdir)/.venv.done.log \
  $(top_srcdir)/etc/domain_directories.tsv \
  $(top_srcdir)/etc/dependency_files.tsv \
  $(top_srcdir)/ontology/catalog-v001.xml \
  $(uco_srcdir)/src/create-catalog-v001.xml.py \
  $(uco_srcdir)/ontology/uco/master/catalog-v001.xml \
  shapes.ttl
	rm -f _$@
	source $(top_srcdir)/venv/bin/activate \
	  && python3 $(uco_srcdir)/src/create-catalog-v001.xml.py \
	    --catalog-xml $(case_srcdir)/ontology/master/catalog-v001.xml \
	    --catalog-xml $(top_srcdir)/ontology/catalog-v001.xml \
	    --catalog-xml $(uco_srcdir)/ontology/uco/master/catalog-v001.xml \
	    _$@ \
	    $(top_srcdir)/etc/domain_directories.tsv \
	    $(top_srcdir)/etc/dependency_files.tsv \
	    "$(top_srcdir)" \
	    shapes.ttl
	mv _$@ $@

check: \
  $(check_shape_targets) \
  uco_owl_review.ttl \
  validate_inheritance.ttl

check-%.ttl: \
  %.ttl \
  .check-%.ttl
	diff $^	\
	  || (echo "ERROR:Makefile:The local $< does not match the normalized version. If the above reported changes look fine, run 'cp .check-$< $<' while in the sub-folder shapes/ to get a file ready to commit to Git." >&2 ; exit 1)

clean:
	@rm -f \
	  $(check_shape_files) \
	  shapes.ttl \
	  uco_owl_review.ttl \
	  validate_inheritance.ttl

shapes.ttl: \
  $(top_srcdir)/.venv.done.log \
  $(shapes_ttl_sources)
	source $(top_srcdir)/venv/bin/activate \
	  && rdfpipe \
	    --output-format turtle \
	    $(shapes_ttl_sources) \
	    > __$@
	java -jar $(top_srcdir)/dependencies/CASE/dependencies/UCO/lib/rdf-toolkit.jar \
	  --inline-blank-nodes \
	  --source __$@ \
	  --source-format turtle \
	  --target _$@ \
	  --target-format turtle
	rm __$@
	mv _$@ $@

uco_owl_review.ttl: \
  $(top_srcdir)/dependencies/dependencies.ttl \
  $(top_srcdir)/ontology/case-corpora.ttl \
  $(top_srcdir)/.venv.done.log \
  local.ttl \
  shapes.ttl
	source $(top_srcdir)/venv/bin/activate \
	  && case_validate \
	    --allow-infos \
	    --format turtle \
	    --metashacl \
	    --ontology-graph $(top_srcdir)/dependencies/dependencies.ttl \
	    --ontology-graph $(top_srcdir)/ontology/case-corpora.ttl \
	    --ontology-graph local.ttl \
	    --ontology-graph shapes.ttl \
	    --review-tbox \
	    $(top_srcdir)/dependencies/CASE/dependencies/UCO/tests/thing.ttl \
	    > _$@
	mv _$@ $@

validate_inheritance.ttl: \
  $(top_srcdir)/dependencies/dependencies.ttl \
  $(top_srcdir)/ontology/case-corpora.ttl \
  $(top_srcdir)/.venv.done.log \
  local.ttl \
  shapes.ttl
	rm -f _$@
	source $(top_srcdir)/venv/bin/activate \
	  && case_shacl_inheritance_reviewer \
	    --debug \
	    _$@ \
	    $(top_srcdir)/dependencies/dependencies.ttl \
	    $(top_srcdir)/ontology/case-corpora.ttl \
	    local.ttl \
	    shapes.ttl
	mv _$@ $@
