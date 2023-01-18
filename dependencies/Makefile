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

case_develop_ttls := \
  $(wildcard CASE-develop/ontology/*/*.ttl) \
  $(wildcard UCO-develop/ontology/*/*.ttl) \
  $(wildcard UCO-develop/ontology/uco/*/*.ttl)

case_unstable_ttls := \
  $(wildcard CASE-unstable/ontology/*/*.ttl) \
  $(wildcard UCO-unstable/ontology/*/*.ttl) \
  $(wildcard UCO-unstable/ontology/uco/*/*.ttl)

dependent_ontology_files := \
  dc.ttl \
  dcat.ttl \
  dcterms.ttl \
  dublin_core_type.ttl \
  vcard.ttl

rdf_toolkit_jar := $(top_srcdir)/dependencies/CASE/dependencies/UCO/lib/rdf-toolkit.jar

all: \
  CASE-develop.ttl \
  CASE-unstable.ttl \
  dcat-us.jsonld \
  dependencies.ttl

CASE-develop.ttl: \
  $(top_srcdir)/.venv.done.log \
  $(case_develop_ttls)
	rm -f _$@
	source $(top_srcdir)/venv/bin/activate \
	  && rdfpipe \
	    --output-format turtle \
	    $(case_develop_ttls) \
	    > _$@
	mv _$@ $@

CASE-unstable.ttl: \
  $(top_srcdir)/.venv.done.log \
  $(case_unstable_ttls)
	rm -f _$@
	source $(top_srcdir)/venv/bin/activate \
	  && rdfpipe \
	    $(case_unstable_ttls) \
	    > _$@
	mv _$@ $@

clean:
	@rm -f \
	  dependencies.ttl

# http://purl.org/dc/elements/1.1
#   via https://www.dublincore.org/schemas/rdfs/
dc.ttl:
	wget \
	  --output-document=__$@ \
	  https://www.dublincore.org/specifications/dublin-core/dcmi-terms/dublin_core_elements.ttl
	java -jar $(rdf_toolkit_jar) \
	  --inline-blank-nodes \
	  --source-format turtle \
	  --source __$@ \
	  --target-format turtle \
	  --target _$@
	rm __$@
	mv _$@ $@

dcat.ttl:
	wget \
	  --output-document=__$@ \
	  https://www.w3.org/ns/dcat.ttl
	java -jar $(rdf_toolkit_jar) \
	  --inline-blank-nodes \
	  --source-format turtle \
	  --source __$@ \
	  --target-format turtle \
	  --target _$@
	rm __$@
	mv _$@ $@

# https://resources.data.gov/resources/dcat-us/#context
dcat-us.jsonld:
	wget \
	  --output-document=_$@ \
	  https://project-open-data.cio.gov/v1.1/schema/catalog.jsonld
	mv _$@ $@

dcterms.ttl:
	wget \
	  --header 'Accept: text/turtle' \
	  --output-document=__$@ \
	  http://purl.org/dc/terms/
	java -jar $(rdf_toolkit_jar) \
	  --inline-blank-nodes \
	  --source-format turtle \
	  --source __$@ \
	  --target-format turtle \
	  --target _$@
	rm __$@
	mv _$@ $@

dependencies.ttl: \
  $(top_srcdir)/.venv.done.log \
  $(dependent_ontology_files)
	source $(top_srcdir)/venv/bin/activate \
	  && rdfpipe \
	    --output-format turtle \
	    $(dependent_ontology_files) \
	    > __$@
	java -jar $(rdf_toolkit_jar) \
	  --inline-blank-nodes \
	  --source-format turtle \
	  --source __$@ \
	  --target-format turtle \
	  --target _$@
	rm __$@
	mv _$@ $@

# http://purl.org/dc/dcmitype/
#   via https://www.dublincore.org/schemas/rdfs/
dublin_core_type.ttl:
	wget \
	  --output-document=__$@ \
	  https://www.dublincore.org/specifications/dublin-core/dcmi-terms/dublin_core_type.ttl
	java -jar $(rdf_toolkit_jar) \
	  --inline-blank-nodes \
	  --source-format turtle \
	  --source __$@ \
	  --target-format turtle \
	  --target _$@
	rm __$@
	mv _$@ $@

vcard.ttl:
	wget \
	  --output-document=__$@ \
	  https://www.w3.org/2006/vcard/ns
	java -jar $(rdf_toolkit_jar) \
	  --inline-blank-nodes \
	  --source-format turtle \
	  --source __$@ \
	  --target-format turtle \
	  --target _$@
	rm __$@
	mv _$@ $@
