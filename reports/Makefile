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

all: \
  README.md

README.md: \
  README.md.in \
  README.md.sed \
  apps.md \
  devices.md \
  import_closure.svg \
  mime-types.md
	sed \
	  -f README.md.sed \
	  README.md.in \
	  > _$@
	mv _$@ $@

# No tests yet conceived for this folder.
check:

clean:
	@rm -f \
	  _* \
	  *.dot \
	  *.md \
	  *.svg

apps.md: \
  $(top_srcdir)/catalog/kb-all.ttl \
  apps.sparql
	source $(top_srcdir)/venv/bin/activate \
	  && case_sparql_select \
	    _$@ \
	    apps.sparql \
	    $(top_srcdir)/catalog/kb-all.ttl
	mv _$@ $@

devices.md: \
  $(top_srcdir)/catalog/kb-all.ttl \
  $(top_srcdir)/taxonomy/devices/drafting.ttl \
  devices.sparql
	source $(top_srcdir)/venv/bin/activate \
	  && case_sparql_select \
	    --no-index \
	    _$@ \
	    devices.sparql \
	    $(top_srcdir)/catalog/kb-all.ttl \
	    $(top_srcdir)/taxonomy/devices/drafting.ttl
	mv _$@ $@

import_closure.dot: \
  $(top_srcdir)/.venv.done.log \
  $(top_srcdir)/catalog/catalog.ttl \
  $(top_srcdir)/dependencies/CDO-Shapes-Time/shapes/sh-time.ttl \
  $(top_srcdir)/dependencies/dependencies.ttl \
  $(top_srcdir)/ontology/case-corpora.ttl \
  $(top_srcdir)/shapes/local.ttl \
  $(top_srcdir)/shapes/shapes.ttl \
  $(top_srcdir)/src/import_closure.py
	source $(top_srcdir)/venv/bin/activate \
	  && python3 $(top_srcdir)/src/import_closure.py \
	    $(top_srcdir)/catalog/catalog.ttl \
	    $(top_srcdir)/dependencies/CDO-Shapes-Time/shapes/sh-time.ttl \
	    $(top_srcdir)/dependencies/dependencies.ttl \
	    $(top_srcdir)/ontology/case-corpora.ttl \
	    $(top_srcdir)/shapes/local.ttl \
	    $(top_srcdir)/shapes/shapes.ttl \
	    > _$@
	mv _$@ $@

import_closure.svg: \
  import_closure.dot
	dot -T svg -o _$@ $<
	mv _$@ $@

mime-types.md: \
  $(top_srcdir)/catalog/kb-all.ttl \
  mime-types.sparql
	source $(top_srcdir)/venv/bin/activate \
	  && case_sparql_select \
	    --no-index \
	    _$@ \
	    mime-types.sparql \
	    $(top_srcdir)/catalog/kb-all.ttl
	mv _$@ $@
