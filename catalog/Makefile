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

all:
	$(MAKE) \
	  --directory datasets
	$(MAKE) \
	  --file postvisit.mk

check: \
  validate-catalog.ttl \
  all
	$(MAKE) \
	  --directory datasets \
	  check
	$(MAKE) \
	  --file postvisit.mk \
	  check

clean:
	@rm -f \
	  kb-*.ttl \
	  validate-*.ttl

validate-catalog.ttl: \
  $(top_srcdir)/.venv.done.log \
  $(top_srcdir)/dependencies/dependencies.ttl \
  $(top_srcdir)/shapes/debug.ttl \
  $(top_srcdir)/shapes/shapes.ttl \
  .catalog-example-dataset.ttl \
  catalog.ttl
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
	    catalog.ttl \
	    .catalog-example-dataset.ttl \
	    || (cat _$@ ; exit 1)
	mv _$@ $@
