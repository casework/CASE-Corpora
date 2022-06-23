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

dependent_shape_files := \
  case-corpora.ttl \
  dcat-us.ttl \
  dcat.ttl \
  dct.ttl

all:

check: \
  validate_inheritance.ttl

validate_inheritance.ttl: \
  $(dependent_shape_files) \
  $(top_srcdir)/.venv.done.log
	rm -f _$@
	source $(top_srcdir)/venv/bin/activate \
	  && case_shacl_inheritance_reviewer \
	    --debug \
	    _$@ \
	    $(dependent_shape_files)
	mv _$@ $@
