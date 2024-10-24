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

"""
This script performs RDFS expansion on the input graphs and emits the inferred triples as a new graph.
"""

import argparse

import owlrl  # type: ignore
import rdflib


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("out_graph")
    parser.add_argument("in_graph", nargs="+")
    args = parser.parse_args()

    graph = rdflib.Graph()
    for in_graph in args.in_graph:
        graph.parse(in_graph)
    inferencer = owlrl.DeductiveClosure(owlrl.RDFSClosure.RDFS_Semantics)

    unexpanded_graph = rdflib.Graph()
    unexpanded_graph += graph

    inferencer.expand(graph)

    graph -= unexpanded_graph

    graph.serialize(args.out_graph)


if __name__ == "__main__":
    main()
