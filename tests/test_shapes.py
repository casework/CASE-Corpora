#!/usr/bin/env python3

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

from typing import Set

from rdflib import SH, TIME, Graph, URIRef
from rdflib.query import ResultRow

NS_SH = SH
NS_TIME = TIME


def test_qualified_url_shape() -> None:
    expected: Set[URIRef] = {
        URIRef("http://example.org/kb/url-34d751fd-9039-45fc-87c5-b1cdbfc7ef10"),
        URIRef("http://example.org/kb/url-b51dfe9c-48bf-41a8-97fd-cf139845fa8c"),
        URIRef("http://example.org/kb/url-dd3e2489-37f0-478c-92bb-c45831337dd4"),
    }
    computed: Set[URIRef] = set()

    graph = Graph()
    graph.parse("distribution_XFAIL_validation.ttl")
    query = """\
SELECT ?nFocusNode
WHERE {
  ?nValidationResult
    sh:focusNode ?nFocusNode ;
    sh:sourceConstraintComponent sh:QualifiedMinCountConstraintComponent ;
    .
}
"""
    for result in graph.query(query):
        assert isinstance(result, ResultRow)
        assert isinstance(result[0], URIRef)
        computed.add(result[0])
    assert expected == computed


def _test_owl_abox_XFAIL(inferencing: str, expected: Set[URIRef]) -> None:
    computed: Set[URIRef] = set()

    assert inferencing in {"none", "owlrl", "rdfs"}

    graph = Graph()
    graph.parse("owl_abox_XFAIL_inferencing_%s_validation.ttl" % inferencing)
    for triple in graph.triples((None, NS_SH.focusNode, None)):
        assert isinstance(triple[2], URIRef)
        computed.add(triple[2])
    assert expected == computed


def test_owl_abox_XFAIL_inferencing_none() -> None:
    expected: Set[URIRef] = {
        URIRef("http://example.org/kb/thing-a-nota"),
        URIRef("http://example.org/kb/thing-b-notb"),
    }
    _test_owl_abox_XFAIL("none", expected)


def test_owl_abox_XFAIL_inferencing_owlrl() -> None:
    expected: Set[URIRef] = {
        URIRef("http://example.org/kb/thing-a-nota"),
        URIRef("http://example.org/kb/thing-b-notb"),
        URIRef("http://example.org/kb/thing-nota-suba"),
        URIRef("http://example.org/kb/thing-notb-subb"),
    }
    _test_owl_abox_XFAIL("owlrl", expected)


def test_owl_abox_XFAIL_inferencing_rdfs() -> None:
    expected: Set[URIRef] = {
        URIRef("http://example.org/kb/thing-a-nota"),
        URIRef("http://example.org/kb/thing-b-notb"),
        URIRef("http://example.org/kb/thing-nota-suba"),
        URIRef("http://example.org/kb/thing-notb-subb"),
    }
    _test_owl_abox_XFAIL("rdfs", expected)
