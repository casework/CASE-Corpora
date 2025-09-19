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

# Usage context:
# This is expected to run in directories following this pattern:
# $(top_srcdir)/catalog/datasets/digitalcorpora-$(dataset)/
#
# The Make variable rdf_toolkit_jar is also expected to already have
# been defined before calling.

generated-digitalcorpora-supplement.ttl:  \
  $(top_srcdir)/.venv.done.log \
  $(top_srcdir)/ontology/dependencies.ttl \
  $(top_srcdir)/ontology/case-corpora.ttl \
  $(top_srcdir)/shapes/dependencies.ttl \
  $(top_srcdir)/shapes/local.ttl \
  $(top_srcdir)/shapes/shapes.ttl \
  $(top_srcdir)/src/case_utils_extras.py \
  $(top_srcdir)/src/digital_corpora_supplement_ttl.py \
  $(top_srcdir)/var/digital_corpora_index.tsv \
  digital_corpora_subjects.txt
	rm -f __$@ _$@
	source $(top_srcdir)/venv/bin/activate \
	  && python3 $(top_srcdir)/src/digital_corpora_supplement_ttl.py \
	    --debug \
	    __$@ \
	    $(top_srcdir)/var/digital_corpora_index.tsv \
	    digital_corpora_subjects.txt
	# Skip validation when this file is called in a GitHub action.
	test ! -z "$${GITHUB_ACTIONS+x}" \
	  || ( \
	    source $(top_srcdir)/venv/bin/activate \
	      && case_validate \
	        --allow-infos \
	        --inference rdfs \
	        --ontology-graph $(top_srcdir)/ontology/dependencies.ttl \
	        --ontology-graph $(top_srcdir)/ontology/case-corpora.ttl \
	        --ontology-graph $(top_srcdir)/shapes/dependencies.ttl \
	        --ontology-graph $(top_srcdir)/shapes/local.ttl \
	        --ontology-graph $(top_srcdir)/shapes/shapes.ttl \
	        __$@ \
	    )
	java -jar $(rdf_toolkit_jar) \
	  --inline-blank-nodes \
	  --source-format turtle \
	  --source __$@ \
	  --target-format turtle \
	  --target _$@
	rm __$@
	mv _$@ $@
