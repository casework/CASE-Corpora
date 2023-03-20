#!/usr/bin/env python3

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

import logging

import pytest
import rdflib

NS_KB = rdflib.Namespace("http://example.org/kb/")


@pytest.fixture(scope="session")
def graph() -> rdflib.Graph:
    g = rdflib.Graph()
    g.parse("kb.ttl")
    return g


def ask_derivation(
    graph: rdflib.Graph, n_source: rdflib.URIRef, n_target: rdflib.URIRef
) -> None:
    expected = True
    computed = False

    for result in graph.query(
        """\
ASK {
    ?nTarget prov:wasDerivedFrom* ?nSource .
}
""",
        initBindings={"nSource": n_source, "nTarget": n_target},
    ):
        assert isinstance(result, bool)
        logging.debug(result)
        computed = result

    assert expected == computed


def test_650599c6_to_88c14fff(graph: rdflib.Graph) -> None:
    ask_derivation(
        graph,
        NS_KB["device-650599c6-701f-4f2e-becb-74398b366ba3"],
        NS_KB["distribution-88c14fff-8304-4409-bfd5-db8217461e9b"],
    )


def test_6e718fd4_to_dd871377(graph: rdflib.Graph) -> None:
    ask_derivation(
        graph,
        NS_KB["device-6e718fd4-d876-4f81-8d58-10c21a741a70"],
        NS_KB["distribution-dd871377-7b49-46d7-90ae-564dae8398f7"],
    )


def test_8fe70491_to_3ad744db(graph: rdflib.Graph) -> None:
    ask_derivation(
        graph,
        NS_KB["device-8fe70491-26c5-4226-a735-ccda10e1a73a"],
        NS_KB["distribution-3ad744db-b926-40c1-8edf-2d5f46deb806"],
    )
