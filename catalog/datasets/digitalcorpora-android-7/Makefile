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

extra_supplement_graphs := \
  generated-digitalcorpora-supplement.ttl

include ../../../src/dataset.mk

include ../../../src/digital_corpora_supplement.mk

# Add additional 'all' targets.
all: \
  README.md

README.md: \
  README.md.in \
  README.md.sed \
  filtered-blk0_mmcblk0.bin.activities-entities.svg \
  filtered-blk0_mmcblk0.bin.entities.svg \
  filtered-blk32_mmcblk0rpmb.bin.activities-entities.svg \
  filtered-blk32_mmcblk0rpmb.bin.entities.svg \
  hash_statements.md
	sed \
	  -f README.md.sed \
	  README.md.in \
	  > _$@
	mv _$@ $@

# This file is not retained, instead being manually integrated into supplemental.ttl.
apps.ttl: \
  apps.tsv \
  apps_ttl.py
	source $(top_srcdir)/venv/bin/activate \
	  && python3 apps_ttl.py \
	    _$@
	mv _$@ $@

# Augment generic target
figures: \
  filtered-blk0_mmcblk0.bin.activities-entities.svg \
  filtered-blk0_mmcblk0.bin.entities.svg \
  filtered-blk32_mmcblk0rpmb.bin.activities-entities.svg \
  filtered-blk32_mmcblk0rpmb.bin.entities.svg

filtered-blk0_mmcblk0.bin.activities-entities.dot: \
  filtered-blk0_mmcblk0.bin.activities-entities.ttl
	source $(top_srcdir)/venv/bin/activate \
	  && case_prov_dot \
	    _$@ \
	    $<
	mv _$@ $@

filtered-blk0_mmcblk0.bin.entities.dot: \
  filtered-blk0_mmcblk0.bin.entities.ttl
	source $(top_srcdir)/venv/bin/activate \
	  && case_prov_dot \
	    _$@ \
	    $<
	mv _$@ $@

filtered-blk0_mmcblk0.bin.activities-entities.ttl: \
  $(top_srcdir)/.venv.done.log \
  $(top_srcdir)/src/filter_entity_provenance.py \
  generated-prov.ttl
	source $(top_srcdir)/venv/bin/activate \
	  && python3 $(top_srcdir)/src/filter_entity_provenance.py \
	    --communication \
	    --generators \
	    _$@ \
	    http://example.org/kb/image-a3c3e13d-98ef-4901-b984-81c10142d90e \
	    http://example.org/kb/file-2352f3d0-d02f-40ba-85a4-b00dd97050c8 \
	    generated-prov.ttl \
	    supplemental.ttl
	mv _$@ $@

filtered-blk0_mmcblk0.bin.entities.ttl: \
  $(top_srcdir)/.venv.done.log \
  $(top_srcdir)/src/filter_entity_provenance.py \
  generated-prov.ttl
	source $(top_srcdir)/venv/bin/activate \
	  && python3 $(top_srcdir)/src/filter_entity_provenance.py \
	    _$@ \
	    http://example.org/kb/image-a3c3e13d-98ef-4901-b984-81c10142d90e \
	    http://example.org/kb/file-2352f3d0-d02f-40ba-85a4-b00dd97050c8 \
	    generated-prov.ttl \
	    supplemental.ttl
	mv _$@ $@

filtered-blk32_mmcblk0rpmb.bin.activities-entities.dot: \
  filtered-blk32_mmcblk0rpmb.bin.activities-entities.ttl
	source $(top_srcdir)/venv/bin/activate \
	  && case_prov_dot \
	    _$@ \
	    $<
	mv _$@ $@

filtered-blk32_mmcblk0rpmb.bin.entities.dot: \
  filtered-blk32_mmcblk0rpmb.bin.entities.ttl
	source $(top_srcdir)/venv/bin/activate \
	  && case_prov_dot \
	    _$@ \
	    $<
	mv _$@ $@

filtered-blk32_mmcblk0rpmb.bin.activities-entities.ttl: \
  $(top_srcdir)/.venv.done.log \
  $(top_srcdir)/src/filter_entity_provenance.py \
  generated-prov.ttl
	source $(top_srcdir)/venv/bin/activate \
	  && python3 $(top_srcdir)/src/filter_entity_provenance.py \
	    --communication \
	    --generators \
	    _$@ \
	    http://example.org/kb/image-9c77c0e9-fd0b-4912-afcf-0d1b1b86f4d6 \
	    http://example.org/kb/file-2352f3d0-d02f-40ba-85a4-b00dd97050c8 \
	    generated-prov.ttl \
	    supplemental.ttl
	mv _$@ $@

filtered-blk32_mmcblk0rpmb.bin.entities.ttl: \
  $(top_srcdir)/.venv.done.log \
  $(top_srcdir)/src/filter_entity_provenance.py \
  generated-prov.ttl
	source $(top_srcdir)/venv/bin/activate \
	  && python3 $(top_srcdir)/src/filter_entity_provenance.py \
	    _$@ \
	    http://example.org/kb/image-9c77c0e9-fd0b-4912-afcf-0d1b1b86f4d6 \
	    http://example.org/kb/file-2352f3d0-d02f-40ba-85a4-b00dd97050c8 \
	    generated-prov.ttl \
	    supplemental.ttl
	mv _$@ $@

hash_statements.md: \
  $(top_srcdir)/.venv.done.log \
  hash_statements.sparql \
  supplemental.ttl
	source $(top_srcdir)/venv/bin/activate \
	  && case_sparql_select \
	    --no-index \
	    --use-prefixes \
	    _$@ \
	    hash_statements.sparql \
	    supplemental.ttl
	mv _$@ $@
