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

dataset_dir_makefiles := $(wildcard */Makefile)

dataset_dirs := $(foreach dataset_dir_makefile,$(dataset_dir_makefiles),$(subst /Makefile,,$(dataset_dir_makefile)))

all_targets := $(foreach dataset_dir,$(dataset_dirs),all-$(dataset_dir))

check_targets := $(foreach dataset_dir,$(dataset_dirs),check-$(dataset_dir))

clean_targets := $(foreach dataset_dir,$(dataset_dirs),clean-$(dataset_dir))

all: \
  $(all_targets)
	@echo $(dataset_dir_makefiles)
	@echo $(dataset_dirs)
	@echo $(all_targets)
	@echo $(check_targets)
	@echo $(clean_targets)

#.PHONY: \
#  $(all_targets) \
#  $(check_targets) \
#  $(clean_targets)

all-%: \
  % \
  $(top_srcdir)/.venv.done.log
	$(MAKE) \
	  --directory $<

check: \
  $(check_targets)

check-%: \
  %
	$(MAKE) \
	  --directory $< \
	  check

clean: \
  $(clean_targets)

clean-%: \
  %
	@$(MAKE) \
	  --directory $< \
	  clean
