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

import re
from typing import Set

from rdflib import Graph, URIRef

RX_UUID = re.compile(
    "[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[0-9a-f]{4}-[0-9a-f]{12}$", re.IGNORECASE
)


def test_android7_hash_iris() -> None:
    """
    To consolidate Hash object references, this script was used to generate UUIDv5s for the Hash IRIs:
    https://github.com/ajnelson-nist/CASE-Examples-QC/blob/main/src/review_hashes.py
    """
    # Expected and computed sets: The sets of Hash IRIs that do not use UUIDv5.
    expected: Set[str] = set()
    computed: Set[str] = set()
    graph = Graph()
    graph.parse("supplemental.ttl")

    query = """\
SELECT ?nHash
WHERE {
    { ?nHash a uco-types:Hash . }
    UNION
    { ?nHash uco-types:hashMethod ?lHashMethod . }
    UNION
    { ?nHash uco-types:hashValue ?lHashValue . }
    UNION
    { ?nContentDataFacet uco-observable:hash ?nHash . }
}
"""
    for result in graph.query(query):
        assert isinstance(result[0], URIRef)
        hash_iri = str(result[0])
        if RX_UUID.search(hash_iri) is None:
            computed.add(hash_iri)
        else:
            if hash_iri[-22] != "5":
                computed.add(hash_iri)

    assert expected == computed
