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

import argparse
import json
import logging
import os
import re
import uuid
from csv import DictReader
from typing import Any, Dict, List, Set
import urllib.parse

from case_utils.namespace import (
    NS_RDF,
    NS_UCO_CORE,
    NS_UCO_OBSERVABLE,
    NS_UCO_TYPES,
    NS_UCO_VOCABULARY,
    NS_XSD,
)
from case_utils_extras import (
    L_SHA256,
    L_SHA3_256,
    method_value_to_node,
)
from rdflib import Graph, Literal, Namespace, URIRef

NS_CASE_CORPORA = Namespace("http://example.org/ontology/case-corpora/")

RX_HEXBINARY = re.compile("^[0-9a-f]+$", re.IGNORECASE)


def n_inherent_facet_for_node(
    n_uco_object: URIRef, n_facet_class: URIRef, ns_kb: Namespace
) -> URIRef:
    uco_object_uuid: uuid.UUID = uuid.uuid5(uuid.NAMESPACE_URL, str(n_uco_object))
    local_has_facet_uuid: uuid.UUID = uuid.uuid5(
        uco_object_uuid, str(NS_UCO_CORE.hasFacet)
    )
    facet_uuid: uuid.UUID = uuid.uuid5(local_has_facet_uuid, str(n_facet_class))

    facet_local_part = str(n_facet_class).split("/")[-1]
    return ns_kb[facet_local_part + "-" + str(facet_uuid)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--prefix", default="http://example.org/kb/")
    parser.add_argument("out_graph")
    parser.add_argument("in_tsv", type=argparse.FileType("r"))
    parser.add_argument(
        "iri_list",
        help="List of IRIs to subset the graph down to.",
        type=argparse.FileType("r"),
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

    NS_KB = Namespace(args.prefix)

    graph = Graph()
    graph.bind("case-corpora", NS_CASE_CORPORA)
    graph.bind("kb", NS_KB)
    graph.bind("uco-core", NS_UCO_CORE)
    graph.bind("uco-observable", NS_UCO_OBSERVABLE)
    graph.bind("uco-types", NS_UCO_TYPES)
    graph.bind("uco-vocabulary", NS_UCO_VOCABULARY)

    n_subjects: Set[URIRef] = set()
    for line in args.iri_list:
        subject_iri = line.strip()
        n_subject = URIRef(subject_iri)
        n_subjects.add(n_subject)

    reader = DictReader(args.in_tsv, delimiter="\t")
    s3_keys_to_disregard: Set[str] = {"corpora/bin/s3_sync.bash"}
    problem_rows: List[Dict[Any, Any]] = []
    for row in reader:
        try:
            if row["s3key"] in s3_keys_to_disregard:
                continue
            if row["s3key"].endswith("~"):
                continue
            n_downloadable_file = URIRef(
                "https://digitalcorpora.s3.amazonaws.com/"
                + urllib.parse.quote(row["s3key"])
            )
            if n_downloadable_file not in n_subjects:
                continue
            n_subjects.remove(n_downloadable_file)

            graph.add(
                (n_downloadable_file, NS_RDF.type, NS_CASE_CORPORA.DownloadableFile)
            )
            graph.add(
                (
                    n_downloadable_file,
                    NS_UCO_CORE.createdBy,
                    NS_KB["organization-72ec45c9-ea94-4503-9428-ad73300056f5"],
                )
            )

            if row["modified"] not in {"None", None}:
                l_object_mtime = Literal(
                    row["modified"].replace(" ", "T") + "Z", datatype=NS_XSD.dateTime
                )
                graph.add(
                    (n_downloadable_file, NS_UCO_CORE.modifiedTime, l_object_mtime)
                )

            n_content_data_facet = n_inherent_facet_for_node(
                n_downloadable_file, NS_UCO_OBSERVABLE.ContentDataFacet, NS_KB
            )
            graph.add(
                (n_content_data_facet, NS_RDF.type, NS_UCO_OBSERVABLE.ContentDataFacet)
            )
            graph.add((n_downloadable_file, NS_UCO_CORE.hasFacet, n_content_data_facet))
            graph.add(
                (
                    n_content_data_facet,
                    NS_UCO_OBSERVABLE.dataPayloadReferenceURL,
                    n_downloadable_file,
                )
            )

            n_file_facet = n_inherent_facet_for_node(
                n_downloadable_file, NS_UCO_OBSERVABLE.FileFacet, NS_KB
            )
            graph.add((n_file_facet, NS_RDF.type, NS_UCO_OBSERVABLE.FileFacet))
            graph.add((n_downloadable_file, NS_UCO_CORE.hasFacet, n_file_facet))

            n_url_facet = n_inherent_facet_for_node(
                n_downloadable_file, NS_UCO_OBSERVABLE.URLFacet, NS_KB
            )
            graph.add((n_url_facet, NS_RDF.type, NS_UCO_OBSERVABLE.URLFacet))
            graph.add((n_downloadable_file, NS_UCO_CORE.hasFacet, n_url_facet))
            graph.add(
                (
                    n_url_facet,
                    NS_UCO_OBSERVABLE.fullValue,
                    Literal(str(n_downloadable_file)),
                )
            )

            graph.add(
                (
                    n_file_facet,
                    NS_UCO_OBSERVABLE.fileName,
                    Literal(os.path.basename(row["s3key"])),
                )
            )
            if row["mtime"] not in {"None", None}:
                l_observable_mtime = Literal(
                    row["mtime"].replace(" ", "T") + "Z", datatype=NS_XSD.dateTime
                )
                graph.add(
                    (n_file_facet, NS_UCO_OBSERVABLE.modifiedTime, l_observable_mtime)
                )

            if row["bytes"] not in {"None", None}:
                l_size_in_bytes = Literal(int(row["bytes"]))
                graph.add(
                    (
                        n_content_data_facet,
                        NS_UCO_OBSERVABLE.sizeInBytes,
                        l_size_in_bytes,
                    )
                )
                graph.add(
                    (n_file_facet, NS_UCO_OBSERVABLE.sizeInBytes, l_size_in_bytes)
                )

            if row["sha2_256"] not in {"None", None}:
                l_hash_value_sha2_256 = Literal(
                    row["sha2_256"], datatype=NS_XSD.hexBinary
                )
                n_hash_sha2_256 = method_value_to_node(
                    L_SHA256, l_hash_value_sha2_256, NS_KB
                )
                graph.add((n_hash_sha2_256, NS_RDF.type, NS_UCO_TYPES.Hash))
                graph.add(
                    (n_content_data_facet, NS_UCO_OBSERVABLE.hash, n_hash_sha2_256)
                )
                graph.add((n_hash_sha2_256, NS_UCO_TYPES.hashMethod, L_SHA256))
                graph.add(
                    (n_hash_sha2_256, NS_UCO_TYPES.hashValue, l_hash_value_sha2_256)
                )

            if row["sha3_256"] not in {"None", None}:
                l_hash_value_sha3_256 = Literal(
                    row["sha3_256"], datatype=NS_XSD.hexBinary
                )
                n_hash_sha3_256 = method_value_to_node(
                    L_SHA3_256, l_hash_value_sha3_256, NS_KB
                )
                graph.add((n_hash_sha3_256, NS_RDF.type, NS_UCO_TYPES.Hash))
                graph.add(
                    (n_content_data_facet, NS_UCO_OBSERVABLE.hash, n_hash_sha3_256)
                )
                graph.add((n_hash_sha3_256, NS_UCO_TYPES.hashMethod, L_SHA3_256))
                graph.add(
                    (n_hash_sha3_256, NS_UCO_TYPES.hashValue, l_hash_value_sha3_256)
                )

            # logging.debug(json.dumps(row, indent=4))
        except ValueError:
            problem_rows.append(row)

    if len(n_subjects) > 0:
        for n_subject in sorted(n_subjects):
            logging.error("* %s", str(n_subject))
        ValueError("Some requested subjects were not in the TSV manifest.")

    for row in problem_rows:
        logging.error(json.dumps(row, indent=4))

    graph.serialize(args.out_graph)


if __name__ == "__main__":
    main()