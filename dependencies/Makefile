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

case_srcdir := CASE

uco_srcdir := $(case_srcdir)/dependencies/UCO

case_develop_ttls := \
  $(wildcard CASE-develop/ontology/*/*.ttl) \
  $(wildcard CASE-develop/dependencies/UCO/ontology/*/*.ttl) \
  $(wildcard CASE-develop/dependencies/UCO/ontology/uco/*/*.ttl)

case_develop_2_0_0_ttls := \
  $(wildcard CASE-develop-2.0.0/ontology/*/*.ttl) \
  $(wildcard CASE-develop-2.0.0/dependencies/UCO/ontology/*/*.ttl) \
  $(wildcard CASE-develop-2.0.0/dependencies/UCO/ontology/uco/*/*.ttl)

case_unstable_ttls := \
  $(wildcard CASE-unstable/ontology/*/*.ttl) \
  $(wildcard CASE-unstable/dependencies/UCO/ontology/*/*.ttl) \
  $(wildcard CASE-unstable/dependencies/UCO/ontology/uco/*/*.ttl)

case_unstable_2_0_0_ttls := \
  $(wildcard CASE-unstable-2.0.0/ontology/*/*.ttl) \
  $(wildcard CASE-unstable-2.0.0/dependencies/UCO/ontology/*/*.ttl) \
  $(wildcard CASE-unstable-2.0.0/dependencies/UCO/ontology/uco/*/*.ttl)

# List of files that house objects of owl:imports triples.  Supports
# local-file resolution by tools that use catalog-v001.xml opening any
# .ttl file within this directory.
dependencies_of_imports_ttl_sources := \
  CDO-Shapes-PROV-O/dependencies/prov-o-dl.ttl \
  CDO-Shapes-Time/dependencies/formatted-time.ttl \
  formatted-cpannotationschema.ttl \
  formatted-dcterms.ttl \
  formatted-situation.ttl \
  formatted-skos.ttl \
  sosa.ttl

# List of all files that house concepts eventually reached by the
# CASE-Corpora transitive imports closure, or closure of any shapes
# files.  Used for confirming presence via Make builds.
dependent_ontology_files := \
  $(dependencies_of_imports_ttl_sources) \
  CDO-Shapes-ORG/dependencies/CDO-Shapes-FOAF/dependencies/formatted-foaf.ttl \
  CDO-Shapes-ORG/dependencies/formatted-org.ttl \
  CDO-Shapes-PROV-O/ontology/cdo-prov-o.ttl \
  discourse-relationships.ttl \
  formatted-cito.ttl \
  formatted-dc.ttl \
  formatted-dcam.ttl \
  formatted-dcat.ttl \
  formatted-dublin_core_type.ttl \
  formatted-vcard.ttl \
  formatted-wgs84_pos.ttl \
  ssn.ttl

rdf_toolkit_jar := $(top_srcdir)/dependencies/CASE/dependencies/UCO/lib/rdf-toolkit.jar

all: \
  CASE-develop.ttl \
  CASE-develop-2.0.0.ttl \
  CASE-unstable.ttl \
  CASE-unstable-2.0.0.ttl \
  $(dependent_ontology_files) \
  catalog-v001.xml \
  dcat-us.jsonld

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

CASE-develop-2.0.0.ttl: \
  $(top_srcdir)/.venv.done.log \
  $(case_develop_2_0_0_ttls)
	rm -f _$@
	source $(top_srcdir)/venv/bin/activate \
	  && rdfpipe \
	    --output-format turtle \
	    $(case_develop_2_0_0_ttls) \
	    > _$@
	mv _$@ $@

CASE-unstable.ttl: \
  $(top_srcdir)/.venv.done.log \
  $(case_unstable_ttls)
	rm -f _$@
	source $(top_srcdir)/venv/bin/activate \
	  && rdfpipe \
	    --output-format turtle \
	    $(case_unstable_ttls) \
	    > _$@
	mv _$@ $@

CASE-unstable-2.0.0.ttl: \
  $(top_srcdir)/.venv.done.log \
  $(case_unstable_2_0_0_ttls)
	rm -f _$@
	source $(top_srcdir)/venv/bin/activate \
	  && rdfpipe \
	    --output-format turtle \
	    $(case_unstable_2_0_0_ttls) \
	    > _$@
	mv _$@ $@

# The `catalog-v001.xml` file in this directory sets up local-file IRI
# resolutions just for files with owl:imports directives.  The full set
# of ontology (/"tbox") local-file resolutions are in
# `/ontology/catalog-v001.xml`, and the full set of shape local-file
# resolutions are in `/shapes/catalog-v001.xml`.
catalog-v001.xml: \
  $(case_srcdir)/ontology/master/catalog-v001.xml \
  $(top_srcdir)/.venv.done.log \
  $(top_srcdir)/etc/domain_directories.tsv \
  $(top_srcdir)/etc/dependency_files.tsv \
  $(uco_srcdir)/src/create-catalog-v001.xml.py \
  $(uco_srcdir)/ontology/uco/master/catalog-v001.xml \
  generated-dependencies_of_imports.ttl
	rm -f _$@
	source $(top_srcdir)/venv/bin/activate \
	  && python3 $(uco_srcdir)/src/create-catalog-v001.xml.py \
	    --catalog-xml $(case_srcdir)/ontology/master/catalog-v001.xml \
	    --catalog-xml $(uco_srcdir)/ontology/uco/master/catalog-v001.xml \
	    _$@ \
	    $(top_srcdir)/etc/domain_directories.tsv \
	    $(top_srcdir)/etc/dependency_files.tsv \
	    "$(top_srcdir)" \
	    generated-dependencies_of_imports.ttl
	mv _$@ $@

check: \
  $(dependent_ontology_files) \
  catalog-v001.xml

clean:
	@rm -f \
	  CASE-develop.ttl \
	  CASE-unstable.ttl \
	  catalog-v001.xml \
	  formatted-dependencies.ttl

# https://resources.data.gov/resources/dcat-us/#context
dcat-us.jsonld:
	wget \
	  --output-document=_$@ \
	  https://project-open-data.cio.gov/v1.1/schema/catalog.jsonld
	mv _$@ $@

# TODO - This does not regenerate with Make while a correction for a term issue is waiting to be published.
discourse-relationships.ttl:
	java -jar $(rdf_toolkit_jar) \
	  --inline-blank-nodes \
	  --source-format rdf-xml \
	  --source swan-ontology/discourse-relationships.owl \
	  --target-format turtle \
	  --target _$@
	mv _$@ $@

formatted-cito.ttl: \
  cito/docs/current/cito.ttl
	java -jar $(rdf_toolkit_jar) \
	  --inline-blank-nodes \
	  --source-format turtle \
	  --source $< \
	  --target-format turtle \
	  --target _$@
	mv _$@ $@

formatted-cpannotationschema.ttl:
	wget \
	  --output-document=__$@ \
	  http://www.ontologydesignpatterns.org/schemas/cpannotationschema.owl
	java -jar $(rdf_toolkit_jar) \
	  --inline-blank-nodes \
	  --source-format rdf-xml \
	  --source __$@ \
	  --target-format turtle \
	  --target _$@
	rm __$@
	mv _$@ $@

# http://purl.org/dc/elements/1.1
#   via https://www.dublincore.org/schemas/rdfs/
formatted-dc.ttl:
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

formatted-dcam.ttl:
	wget \
	  --header 'Accept: text/turtle' \
	  --output-document=__$@ \
	  http://purl.org/dc/dcam/
	java -jar $(rdf_toolkit_jar) \
	  --inline-blank-nodes \
	  --source-format turtle \
	  --source __$@ \
	  --target-format turtle \
	  --target _$@
	rm __$@
	mv _$@ $@

formatted-dcat.ttl:
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

formatted-dcterms.ttl:
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

# http://purl.org/dc/dcmitype/
#   via https://www.dublincore.org/schemas/rdfs/
formatted-dublin_core_type.ttl:
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

formatted-situation.ttl:
	wget \
	  --output-document=__$@ \
	  http://www.ontologydesignpatterns.org/cp/owl/situation.owl
	java -jar $(rdf_toolkit_jar) \
	  --inline-blank-nodes \
	  --source-format rdf-xml \
	  --source __$@ \
	  --target-format turtle \
	  --target _$@
	rm __$@
	mv _$@ $@

formatted-skos.ttl:
	wget \
	  --output-document=__$@ \
	  http://www.w3.org/2004/02/skos/core
	java -jar $(rdf_toolkit_jar) \
	  --inline-blank-nodes \
	  --source-format rdf-xml \
	  --source __$@ \
	  --target-format turtle \
	  --target _$@
	rm __$@
	mv _$@ $@

formatted-vcard.ttl:
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

formatted-wgs84_pos.ttl:
	wget \
	  --output-document=__$@ \
	  https://www.w3.org/2003/01/geo/wgs84_pos
	java -jar $(rdf_toolkit_jar) \
	  --inline-blank-nodes \
	  --source-format rdf-xml \
	  --source __$@ \
	  --target-format turtle \
	  --target _$@
	rm __$@
	mv _$@ $@

generated-dependencies_of_imports.ttl: \
  $(top_srcdir)/.venv.done.log \
  $(dependencies_of_imports_ttl_sources)
	source $(top_srcdir)/venv/bin/activate \
	  && rdfpipe \
	    --output-format turtle \
	    $(dependencies_of_imports_ttl_sources) \
	    > __$@
	java -jar $(rdf_toolkit_jar) \
	  --inline-blank-nodes \
	  --source-format turtle \
	  --source __$@ \
	  --target-format turtle \
	  --target _$@
	rm __$@
	mv _$@ $@

# TODO - This does not regenerate with Make while a correction for this issue is waiting to be published.
# https://github.com/w3c/sdw/issues/1395
sosa.ttl:
	java -jar $(rdf_toolkit_jar) \
	  --inline-blank-nodes \
	  --source-format turtle \
	  --source sdw/ssn/integrated/sosa.ttl \
	  --target-format turtle \
	  --target _$@
	mv _$@ $@

# TODO - This does not regenerate with Make while a correction for this issue is waiting to be published.
# https://github.com/w3c/sdw/issues/1395
ssn.ttl:
	java -jar $(rdf_toolkit_jar) \
	  --inline-blank-nodes \
	  --source-format turtle \
	  --source sdw/ssn/integrated/ssn.ttl \
	  --target-format turtle \
	  --target _$@
	mv _$@ $@
