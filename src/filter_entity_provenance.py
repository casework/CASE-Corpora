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
This script takes as input the IRI of a prov:Entity, the IRI of a second prov:Entity, and a graph containing provenance that links the two.  The graph is filtered to the history starting at the first Entity and ending at the second.  A graph containinly only the linking PROV-O triples is returned as output.  The graph resulting from this script is able to present a more focused illustration of the two entities' provenantial link.

This script was written for a CASE-Corpora workflow, assuming a CASE graph would have a PROV-O graph derived from it using case_prov_rdf, and at least both of those graphs would be used as inputs to this script.
"""

import argparse
import logging
from typing import Dict, Set

from case_utils.namespace import NS_RDF, NS_RDFS, NS_UCO_CORE
from rdflib import PROV, Graph, Namespace, URIRef

NS_KB = Namespace("http://example.org/kb/")
NS_PROV = PROV


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--communication", action="store_true")
    parser.add_argument("--generators", action="store_true")
    parser.add_argument("out_file")
    parser.add_argument("start_iri")
    parser.add_argument("end_iri")
    parser.add_argument("in_graph", nargs="+")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)

    in_graph = Graph()
    out_graph = Graph()
    out_graph.bind("kb", NS_KB)
    out_graph.bind("prov", NS_PROV)
    out_graph.bind("uco-core", NS_UCO_CORE)

    for in_graph_file in args.in_graph:
        in_graph.parse(in_graph_file)
    logging.debug(len(in_graph))

    n_start = URIRef(args.start_iri)
    n_end = URIRef(args.end_iri)

    start_iri_found_in_graph = False
    for triple in in_graph.triples((n_start, NS_RDF.type, None)):
        start_iri_found_in_graph = True
    assert start_iri_found_in_graph, "Requested start IRI is not in the graph."

    end_iri_found_in_graph = False
    for triple in in_graph.triples((n_end, NS_RDF.type, None)):
        end_iri_found_in_graph = True
    assert end_iri_found_in_graph, "Requested end IRI is not in the graph."

    initial_bindings: Dict[str, URIRef] = {"nEnd": n_end, "nStart": n_start}

    # Filter query to entities between start and end.
    query = """\
PREFIX prov: <http://www.w3.org/ns/prov#>
CONSTRUCT {
  ?nLater prov:wasDerivedFrom ?nEarlier .
} WHERE {
  ?nEnd prov:wasDerivedFrom* ?nLater .
  ?nLater prov:wasDerivedFrom ?nEarlier .
  ?nEarlier prov:wasDerivedFrom* ?nStart .
}
"""
    n_found_nodes: Set[URIRef] = set()
    for result in in_graph.query(query, initBindings=initial_bindings):
        assert isinstance(result, tuple)
        assert isinstance(result[0], URIRef)
        assert isinstance(result[1], URIRef)
        assert isinstance(result[2], URIRef)
        for triple in in_graph.triples((result[0], result[1], result[2])):
            assert isinstance(triple[0], URIRef)
            assert isinstance(triple[2], URIRef)
            n_found_nodes.add(triple[0])
            n_found_nodes.add(triple[2])
            out_graph.add(triple)
    for n_found_node in n_found_nodes:
        for triple in in_graph.triples((n_found_node, NS_UCO_CORE.description, None)):
            out_graph.add((n_found_node, NS_RDFS.comment, triple[2]))
        for n_prov_type in {NS_PROV.Entity, NS_PROV.Collection}:
            for triple in in_graph.triples((n_found_node, NS_RDF.type, n_prov_type)):
                out_graph.add(triple)
    if len(out_graph) == 0:
        raise ValueError("The input and output nodes are not provenantially linked.")
    logging.debug(len(out_graph))

    # Include ProvenanceRecords
    for triple0 in out_graph.triples((None, NS_RDF.type, NS_PROV.Collection)):
        for triple1 in in_graph.triples((triple0[0], NS_PROV.hadMember, None)):
            for triple2 in out_graph.triples((triple1[2], NS_RDF.type, NS_PROV.Entity)):
                out_graph.add(triple1)
    logging.debug(len(out_graph))

    n_entities: Set[URIRef] = set()
    for triple in out_graph.triples((None, NS_RDF.type, NS_PROV.Entity)):
        assert isinstance(triple[0], URIRef)
        n_entities.add(triple[0])

    # Include generating Activities.
    if args.generators:
        for triple0 in out_graph.triples((None, NS_RDF.type, NS_PROV.Entity)):
            for triple1 in in_graph.triples((triple0[0], NS_PROV.wasGeneratedBy, None)):
                out_graph.add(triple1)
                out_graph.add((triple1[2], NS_RDF.type, NS_PROV.Activity))
                for triple2 in in_graph.triples((triple1[2], NS_RDFS.comment, None)):
                    out_graph.add(triple2)
                    for n_entity in n_entities:
                        for triple3 in in_graph.triples(
                            (triple1[2], NS_PROV.used, n_entity)
                        ):
                            out_graph.add(triple3)

    n_activities: Set[URIRef] = set()
    for triple in out_graph.triples((None, NS_RDF.type, NS_PROV.Activity)):
        assert isinstance(triple[0], URIRef)
        n_activities.add(triple[0])

    # Include communication links for all in-graph activities that have both communication ends in out-graph.
    if args.communication:
        for n_activity_1 in sorted(n_activities):
            for n_activity_2 in sorted(n_activities):
                for triple in in_graph.triples((n_activity_1, None, n_activity_2)):
                    out_graph.add(triple)

    out_graph.serialize(args.out_file)


if __name__ == "__main__":
    main()
