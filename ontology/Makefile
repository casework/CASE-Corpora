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

# TODO - After release of CASE 1.2.0, have this reference a different submodule.
case_srcdir := $(top_srcdir)/dependencies/CASE-unstable

uco_srcdir := $(case_srcdir)/dependencies/UCO

ontology_files := case-corpora.ttl
check_ontology_files := $(foreach ontology_file,$(ontology_files),.check-$(ontology_file))
check_ontology_targets := $(foreach ontology_file,$(ontology_files),check-$(ontology_file))

all: \
  catalog-v001.xml

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
  $(uco_srcdir)/src/create-catalog-v001.xml.py \
  $(uco_srcdir)/ontology/uco/master/catalog-v001.xml \
  $(ontology_files)
	rm -f _$@
	source $(top_srcdir)/venv/bin/activate \
	  && python3 $(uco_srcdir)/src/create-catalog-v001.xml.py \
	    --catalog-xml $(case_srcdir)/ontology/master/catalog-v001.xml \
	    --catalog-xml $(uco_srcdir)/ontology/uco/master/catalog-v001.xml \
	    _$@ \
	    $(top_srcdir)/etc/domain_directories.tsv \
	    $(top_srcdir)/etc/dependency_files.tsv \
	    "$(top_srcdir)" \
	    $(ontology_files)
	mv _$@ $@

check: \
  $(check_ontology_targets) \
  catalog-v001.xml \
  uco_owl_review.ttl

check-%.ttl: \
  %.ttl \
  .check-%.ttl
	diff $^	\
	  || (echo "ERROR:Makefile:The local $< does not match the normalized version. If the above reported changes look fine, run 'cp .check-$< $<' while in the sub-folder ontology/ to get a file ready to commit to Git." >&2 ; exit 1)

clean:
	@rm -f \
	  $(check_ontology_files) \
	  catalog-v001.xml \
	  uco_owl_review.ttl

uco_owl_review.ttl: \
  $(top_srcdir)/dependencies/dependencies.ttl \
  $(top_srcdir)/.venv.done.log \
  case-corpora.ttl
	source $(top_srcdir)/venv/bin/activate \
	  && case_validate \
	    --allow-infos \
	    --format turtle \
	    --metashacl \
	    --ontology-graph $(top_srcdir)/dependencies/dependencies.ttl \
	    --ontology-graph case-corpora.ttl \
	    $(top_srcdir)/dependencies/CASE/dependencies/UCO/tests/thing.ttl \
	    > _$@
	mv _$@ $@
