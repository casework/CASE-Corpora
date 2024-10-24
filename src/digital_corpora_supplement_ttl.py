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

import argparse
import json
import logging
import os
import re
import uuid
from csv import DictReader
from typing import Any, Dict, List, Optional, Set
import urllib.parse

from case_utils.namespace import (
    NS_RDF,
    NS_UCO_CORE,
    NS_UCO_OBSERVABLE,
    NS_UCO_TYPES,
    NS_UCO_VOCABULARY,
    NS_XSD,
)
from case_utils.inherent_uuid import (
    L_SHA256,
    L_SHA3_256,
    get_facet_uriref,
    inherence_uuid,
)
from case_utils_extras import method_value_to_node
from rdflib import Graph, Literal, Namespace, URIRef

NS_CASE_CORPORA = Namespace("http://example.org/ontology/case-corpora/")
NS_DRAFTING = Namespace("http://example.org/ontology/drafting/")

RX_HEXBINARY = re.compile("^[0-9a-f]+$", re.IGNORECASE)


def characterize_url(graph: Graph, n_thing: URIRef, ns_kb: Namespace) -> URIRef:
    """
    Guarantee URLFacet is present.  Populate, if not found already defined.

    :returns: Returns generated observable:URL IRI.
    """
    url_uuid = uuid.uuid5(uuid.NAMESPACE_URL, str(n_thing))
    n_url = ns_kb["URL-" + str(url_uuid)]
    n_url_facet: Optional[URIRef] = None
    for n_object in graph.objects(n_url, NS_UCO_CORE.hasFacet):
        assert isinstance(n_object, URIRef)
        for triple in graph.triples(
            (n_object, NS_RDF.type, NS_UCO_OBSERVABLE.URLFacet)
        ):
            n_url_facet = n_object
    if n_url_facet is None:
        n_url_facet = get_facet_uriref(
            n_url, NS_UCO_OBSERVABLE.URLFacet, namespace=ns_kb
        )
        graph.add((n_url, NS_UCO_CORE.hasFacet, n_url_facet))
        graph.add((n_url_facet, NS_RDF.type, NS_UCO_OBSERVABLE.URLFacet))
        graph.add((n_url_facet, NS_UCO_OBSERVABLE.fullValue, Literal(str(n_thing))))
    return n_url


def get_digital_corpora_sends_relation(
    graph: Graph,
    n_downloadable_object: URIRef,
    n_s3_object: URIRef,
    namespace: Namespace,
) -> URIRef:
    """
    :returns: Returns a deterministic IRI for an S3Object's mapping to an HTTPS URL.
    """
    uuid0 = inherence_uuid(n_downloadable_object)
    uuid1 = uuid.uuid5(uuid0, str(n_s3_object))
    uuid2 = uuid.uuid5(uuid1, "Sends")
    n_relationship = namespace["ObservableRelationship-" + str(uuid2)]
    graph.add((n_relationship, NS_RDF.type, NS_UCO_OBSERVABLE.ObservableRelationship))
    graph.add((n_relationship, NS_UCO_CORE.isDirectional, Literal(True)))
    graph.add((n_relationship, NS_UCO_CORE.kindOfRelationship, Literal("Sends")))
    graph.add((n_relationship, NS_UCO_CORE.source, n_downloadable_object))
    graph.add((n_relationship, NS_UCO_CORE.target, n_s3_object))
    return n_relationship


def get_digital_corpora_downloadable_relation(
    graph: Graph, n_downloadable_object: URIRef, n_url: URIRef, namespace: Namespace
) -> URIRef:
    """
    :returns: Returns a deterministic IRI for an S3Object downloadable by Digital Corpora's directory presentation protocol.
    """
    uuid0 = inherence_uuid(n_downloadable_object)
    uuid1 = uuid.uuid5(uuid0, str(n_url))
    uuid2 = uuid.uuid5(uuid1, "Downloadable_From")
    n_relationship = namespace["DownloadableRelation-" + str(uuid2)]
    graph.add((n_relationship, NS_RDF.type, NS_CASE_CORPORA.DownloadableRelation))
    graph.add((n_relationship, NS_UCO_CORE.isDirectional, Literal(True)))
    graph.add(
        (n_relationship, NS_UCO_CORE.kindOfRelationship, Literal("Downloadable_From"))
    )
    graph.add((n_relationship, NS_UCO_CORE.source, n_downloadable_object))
    graph.add((n_relationship, NS_UCO_CORE.target, n_url))
    return n_relationship


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
    graph.bind("drafting", NS_DRAFTING)
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
            s3key_quoted = urllib.parse.quote(row["s3key"])
            n_s3_object = URIRef("s3://digitalcorpora/" + s3key_quoted)
            n_downloadable_object = URIRef(
                "https://digitalcorpora.s3.amazonaws.com/" + s3key_quoted
            )
            if n_downloadable_object not in n_subjects:
                continue
            n_subjects.remove(n_downloadable_object)

            graph.add((n_s3_object, NS_RDF.type, NS_DRAFTING.S3Object))
            graph.add(
                (n_downloadable_object, NS_RDF.type, NS_CASE_CORPORA.DownloadableObject)
            )
            n_url = characterize_url(graph, n_downloadable_object, NS_KB)
            graph.add((n_url, NS_RDF.type, NS_UCO_OBSERVABLE.URL))
            graph.add(
                (
                    n_s3_object,
                    NS_UCO_CORE.createdBy,
                    NS_KB["organization-72ec45c9-ea94-4503-9428-ad73300056f5"],
                )
            )
            graph.add(
                (
                    n_downloadable_object,
                    NS_UCO_CORE.createdBy,
                    NS_KB["organization-72ec45c9-ea94-4503-9428-ad73300056f5"],
                )
            )

            if row["modified"] not in {"None", None}:
                l_object_mtime = Literal(
                    row["modified"].replace(" ", "T") + "Z", datatype=NS_XSD.dateTime
                )
                graph.add((n_s3_object, NS_UCO_CORE.modifiedTime, l_object_mtime))

            n_content_data_facet = get_facet_uriref(
                n_s3_object, NS_UCO_OBSERVABLE.ContentDataFacet, namespace=NS_KB
            )
            graph.add(
                (n_content_data_facet, NS_RDF.type, NS_UCO_OBSERVABLE.ContentDataFacet)
            )
            graph.add((n_s3_object, NS_UCO_CORE.hasFacet, n_content_data_facet))

            # Tie S3 Object to URL, two ways.
            # First, uco-observable:dataPayloadReferenceURL.
            # Second, DownloadableRelation.
            graph.add(
                (
                    n_content_data_facet,
                    NS_UCO_OBSERVABLE.dataPayloadReferenceURL,
                    n_downloadable_object,
                )
            )
            _ = get_digital_corpora_downloadable_relation(
                graph, n_downloadable_object, n_url, NS_KB
            )
            _ = get_digital_corpora_sends_relation(
                graph, n_downloadable_object, n_s3_object, NS_KB
            )

            n_file_facet = get_facet_uriref(
                n_s3_object, NS_UCO_OBSERVABLE.FileFacet, namespace=NS_KB
            )
            graph.add((n_file_facet, NS_RDF.type, NS_UCO_OBSERVABLE.FileFacet))
            graph.add((n_s3_object, NS_UCO_CORE.hasFacet, n_file_facet))

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
