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

"""
This script takes an OWL ontology graph file as input, and emits a Dot
(Graphviz) file illustrating the ontology's transitive import closure
and noted import-incompatibilities.
"""

__version__ = "0.1.1"

import argparse
import logging
import os
from typing import Dict, List

import pydot  # type: ignore
import rdflib
from rdflib import OWL, RDF, URIRef

_logger = logging.getLogger(os.path.basename(__file__))


def safe_str(in_string: str) -> str:
    return (
        in_string.replace("/", "_")
        .replace(".", "_")
        .replace("-", "_")
        .replace(":", "_")
        .replace("#", "_")
    )


def safe_node_label(in_iri: URIRef) -> str:
    # Implement same quotation-forcing hack as in case_prov_dot.
    return "IRI - " + str(in_iri)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("in_graph", nargs="+")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

    # rdflib graph, vs. pydot graph.
    rgraph = rdflib.Graph()
    pgraph = pydot.Graph()

    for in_graph in args.in_graph:
        _logger.debug("in_graph = %r.", in_graph)
        rgraph.parse(in_graph)

    ontology_reference: Dict[URIRef, pydot.Node] = dict()

    edges: List[pydot.Edge] = []

    for triple in rgraph.triples((None, RDF.type, OWL.Ontology)):
        assert isinstance(triple[0], URIRef)
        ontology_reference[triple[0]] = pydot.Node(
            safe_str(str(triple[0])), label=safe_node_label(triple[0])
        )
    for triple in rgraph.triples((None, OWL.versionIRI, None)):
        assert isinstance(triple[2], URIRef)
        ontology_reference[triple[2]] = pydot.Node(
            safe_str(str(triple[2])), color="gray", label=safe_node_label(triple[2])
        )
    for triple_pattern in [
        (None, OWL.imports, None),
        (None, OWL.incompatibleWith, None),
        (None, OWL.priorVersion, None),
        (None, OWL.versionIRI, None),
    ]:
        for triple in rgraph.triples(triple_pattern):
            # OWL permits the ontology IRI to be a blank node.
            if not isinstance(triple[0], URIRef):
                continue
            # OWL might permit the object of this triple to be a blank node,
            # but the assumption for now is that this is a data error.
            assert isinstance(triple[2], URIRef)
            if triple[0] not in ontology_reference:
                ontology_reference[triple[0]] = pydot.Node(
                    safe_str(str(triple[0])), label=safe_node_label(triple[0])
                )
            if triple[2] not in ontology_reference:
                ontology_reference[triple[2]] = pydot.Node(
                    safe_str(str(triple[2])), label=safe_node_label(triple[2])
                )
            edge_label = str(triple_pattern[1]).replace(str(OWL), "")

            edge_style = (
                "dashed"
                if triple_pattern[1] in {OWL.incompatibleWith, OWL.priorVersion}
                else ""
            )

            edge_color = ""
            edge_fontcolor = ""
            if triple_pattern[1] == OWL.incompatibleWith:
                edge_color = "red"
                edge_fontcolor = "red"
            elif triple_pattern[1] in {OWL.priorVersion, OWL.versionIRI}:
                edge_color = "gray"

            edge = pydot.Edge(
                ontology_reference[triple[0]],
                ontology_reference[triple[2]],
                color=edge_color,
                fontcolor=edge_fontcolor,
                label=edge_label,
                style=edge_style,
            )
            edges.append(edge)

    for ontology_pnode in ontology_reference.values():
        pgraph.add_node(ontology_pnode)
    for edge in edges:
        pgraph.add_edge(edge)

    print(str(pgraph))


if __name__ == "__main__":
    main()
