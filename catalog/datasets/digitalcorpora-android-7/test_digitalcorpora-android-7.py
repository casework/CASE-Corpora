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
import warnings
from typing import Set

from rdflib import PROV, Graph, Literal, URIRef

NS_PROV = PROV

RX_UUID = re.compile(
    "[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[0-9a-f]{4}-[0-9a-f]{12}$", re.IGNORECASE
)


def test_android7_distribution_inputs_and_outputs_matched() -> None:
    """
    This test confirms the files extracted from the downloaded distribution tarball can map to a file that was gathered into the pre-upload distribution tarball.
    """
    # Consider the files extracted from the downloaded tarball to be the "Expected" set.
    # The "Computed" set is then the file nodes where a history has been constructed.
    expected: Set[str] = set()
    computed: Set[str] = set()

    graph = Graph()
    graph.parse("kb.ttl")
    query_extracted = """\
SELECT ?lFileName
WHERE {
?nFile
  prov:wasGeneratedBy kb:investigative-action-194c4e23-243e-4deb-b8d5-3ce9dce19367 ;
  uco-core:hasFacet / uco-observable:fileName ?lFileName ;
  .
}
"""
    query_packaged = """\
SELECT ?lFileName
WHERE {
kb:file-2352f3d0-d02f-40ba-85a4-b00dd97050c8
  prov:wasDerivedFrom ?nFile ;
  .

?nFile
  uco-core:hasFacet / uco-observable:fileName ?lFileName ;
  .
}
"""

    for result_extracted in graph.query(query_extracted):
        assert isinstance(result_extracted[0], Literal)
        expected.add(str(result_extracted[0]))
    assert len(expected) > 0

    for result_packaged in graph.query(query_packaged):
        assert isinstance(result_packaged[0], Literal)
        computed.add(str(result_packaged[0]))

    try:
        assert expected == computed
    except AssertionError:
        warnings.warn(
            "Some files extracted from distribution tarball are not noted in the tarball's history."
        )
        # TODO - Uncomment once file nodes are defined and pass case_prov_check.
        # raise


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
