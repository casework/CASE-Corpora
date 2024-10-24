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

top_srcdir := $(shell cd ../.. ; pwd)

taxonomy_files := drafting.ttl
check_taxonomy_files := $(foreach taxonomy_file,$(taxonomy_files),.check-$(taxonomy_file))
check_taxonomy_targets := $(foreach taxonomy_file,$(taxonomy_files),check-$(taxonomy_file))

all:

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

check: \
  $(check_taxonomy_targets)

check-%.ttl: \
  %.ttl \
  .check-%.ttl
	diff $^	\
	  || (echo "ERROR:Makefile:The local $< does not match the normalized version. If the above reported changes look fine, run 'cp .check-$< $<' while in the sub-folder taxonomy/devices/ to get a file ready to commit to Git." >&2 ; exit 1)

clean:
	@rm -f \
	  $(check_taxonomy_files)
