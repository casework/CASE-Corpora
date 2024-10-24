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

digital_corpora_subjects_txts := $(wildcard $(top_srcdir)/catalog/datasets/digitalcorpora-*/digital_corpora_subjects.txt)

all: \
  digital_corpora_index.tsv

check: \
  digital_corpora_index.tsv

clean:
	@rm -f \
	  _* \
	  cached-digital_corpora_index.tsv \
	  generated-digital_corpora_index.tsv

# The top-level Make orchestration is designed to run this recipe only
# infrequently, and in local development environments.  See the
# 'all-var' target in $(top_srcdir)/Makefile.
# 
# This recipe is expected to re-run after a 'make clean' when not in a
# GitHub Action.
cached-digital_corpora_index.tsv:
	wget \
	  --output-document _$@ \
	  https://downloads.digitalcorpora.org/index.tsv
	mv _$@ $@

digital_corpora_index.tsv: \
  $(top_srcdir)/src/filter_digital_corpora_index_tsv.py \
  cached-digital_corpora_index.tsv \
  generated-digital_corpora_subjects.txt
	rm -f _$@
	python3 $(top_srcdir)/src/filter_digital_corpora_index_tsv.py \
	  cached-digital_corpora_index.tsv \
	  generated-digital_corpora_subjects.txt \
	  _$@
	mv _$@ $@

generated-digital_corpora_subjects.txt: \
  $(digital_corpora_subjects_txts)
	rm -f _$@
	touch _$@
	test -z "$^" \
	  || cat $^ | sort | uniq > _$@
	mv _$@ $@
