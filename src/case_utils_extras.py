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
This library provides supporting constants and functions for generating
UUIDv5s for UCO Hash nodes. The UUIDv5 seed data is a URN following the
scheme in this draft IETF memo:

https://datatracker.ietf.org/doc/html/draft-thiemann-hash-urn-01

Note that at the time of this writing, that memo was expired (expiration
date 2004-03-04) and did not have a linked superseding document.
"""

import binascii
import re
import uuid
from typing import Dict, Optional, Tuple

from case_utils.namespace import NS_UCO_VOCABULARY, NS_XSD
from rdflib import Literal, Namespace, URIRef


L_MD5 = Literal("MD5", datatype=NS_UCO_VOCABULARY.HashNameVocab)
L_SHA1 = Literal("SHA1", datatype=NS_UCO_VOCABULARY.HashNameVocab)
L_SHA256 = Literal("SHA256", datatype=NS_UCO_VOCABULARY.HashNameVocab)
L_SHA3_256 = Literal("SHA3-256", datatype=NS_UCO_VOCABULARY.HashNameVocab)
L_SHA384 = Literal("SHA384", datatype=NS_UCO_VOCABULARY.HashNameVocab)
L_SHA512 = Literal("SHA512", datatype=NS_UCO_VOCABULARY.HashNameVocab)
L_SSDEEP = Literal("SSDEEP", datatype=NS_UCO_VOCABULARY.HashNameVocab)

# Key: hashMethod literal.
# Value: Tuple.
#   * Lowercase spelling
# TODO - SHA3-256 is used by Digital Corpora, impacting CASE-Corpora, but the vocabulary string is not yet in UCO.
# https://github.com/ucoProject/UCO/issues/526
HASH_METHOD_CASTINGS: Dict[Literal, Tuple[str, Optional[int]]] = {
    L_MD5: ("md5", 32),
    L_SHA1: ("sha1", 40),
    L_SHA256: ("sha256", 64),
    L_SHA3_256: ("sha3-256", 64),
    L_SHA384: ("sha384", 96),
    L_SHA512: ("sha512", 128),
    L_SSDEEP: ("ssdeep", None),
}

RX_UUID = re.compile(
    "[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[0-9a-f]{4}-[0-9a-f]{12}$", re.IGNORECASE
)


def method_value_to_node(
    l_hash_method: Literal, l_hash_value: Literal, ns_kb: Namespace
) -> URIRef:
    if l_hash_value.datatype != NS_XSD.hexBinary:
        raise ValueError("Expected hexBinary datatype for l_hash_value.")
    hash_value_str: str = binascii.hexlify(l_hash_value.toPython()).decode().lower()

    hash_method_str = HASH_METHOD_CASTINGS[l_hash_method][0]

    urn_template = "urn:hash::%s:%s"
    urn_populated = urn_template % (hash_method_str, hash_value_str)

    hash_uuid = str(uuid.uuid5(uuid.NAMESPACE_URL, urn_populated))
    n_hash = ns_kb["Hash-" + hash_uuid]

    return n_hash


def node_iri_uses_uuid4(n_hash: URIRef) -> bool:
    hash_iri: str = n_hash.toPython()
    if RX_UUID.search(hash_iri) is None:
        return False
    return hash_iri[-22] == "4"
