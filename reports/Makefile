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
  devices.md \
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
	  *.md

devices.md: \
  $(top_srcdir)/catalog/kb-all.ttl \
  $(top_srcdir)/taxonomy/devices/drafting.ttl \
  devices.sparql
	source $(top_srcdir)/venv/bin/activate \
	  && case_sparql_select \
	    _$@ \
	    devices.sparql \
	    $(top_srcdir)/catalog/kb-all.ttl \
	    $(top_srcdir)/taxonomy/devices/drafting.ttl
	mv _$@ $@

mime-types.md: \
  $(top_srcdir)/catalog/kb-all.ttl \
  mime-types.sparql
	source $(top_srcdir)/venv/bin/activate \
	  && case_sparql_select \
	    _$@ \
	    mime-types.sparql \
	    $(top_srcdir)/catalog/kb-all.ttl
	mv _$@ $@
