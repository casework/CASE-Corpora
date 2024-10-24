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
This library provides supporting constants and functions for generating
UUIDv5s for UCO Hash nodes. The UUIDv5 seed data is a URN following the
scheme in this draft IETF memo:

https://datatracker.ietf.org/doc/html/draft-thiemann-hash-urn-01

Note that at the time of this writing, that memo was expired (expiration
date 2004-03-04) and did not have a linked superseding document.
"""

from case_utils.inherent_uuid import (
    RX_UUID,
    hash_method_value_uuid,
)
from rdflib import Literal, Namespace, URIRef


def method_value_to_node(
    l_hash_method: Literal, l_hash_value: Literal, ns_kb: Namespace
) -> URIRef:
    hash_uuid = str(hash_method_value_uuid(l_hash_method, l_hash_value))
    n_hash = ns_kb["Hash-" + hash_uuid]
    return n_hash


def node_iri_uses_uuid4(n_hash: URIRef) -> bool:
    hash_iri: str = n_hash.toPython()
    if RX_UUID.search(hash_iri) is None:
        return False
    return hash_iri[-22] == "4"
