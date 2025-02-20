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

import binascii
import re
import warnings
from typing import Set, Tuple

from rdflib import PROV, Graph, Literal, URIRef
from rdflib.query import ResultRow

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
        assert isinstance(result_extracted, ResultRow)
        assert isinstance(result_extracted[0], Literal)
        expected.add(str(result_extracted[0]))
    assert len(expected) > 0

    for result_packaged in graph.query(query_packaged):
        assert isinstance(result_packaged, ResultRow)
        assert isinstance(result_packaged[0], Literal)
        computed.add(str(result_packaged[0]))

    try:
        assert expected == computed
    except AssertionError:
        warnings.warn(
            "Some files extracted from distribution tarball are not noted in the tarball's history."
        )
        raise


def test_android7_hash_documented_sources() -> None:
    expected: Set[Tuple[str, str, str, str]] = {
        (
            "Android 7 Hashes.pdf",
            "LG GSM_H790 Nexus 5X.ufd",
            "MD5",
            "632286b2d1c6792ea0c83f59e3e12593",
        ),
        (
            "Android 7 Hashes.pdf",
            "LG GSM_H790 Nexus 5X.ufd",
            "SHA1",
            "28679cfa58e1bba24b44b69ae5d10f67b8fd238a",
        ),
        (
            "Android 7 Hashes.pdf",
            "LG GSM_H790 Nexus 5X.ufd",
            "SHA256",
            "6ed61a9271271203c1dd2fea595776db7ea5a625aed3a389e2213f9369175d51",
        ),
        (
            "Android 7 Hashes.pdf",
            "blk0_mmcblk0.bin",
            "MD5",
            "27b7f7389bb2b99ab1b9be04e3bfbbc0",
        ),
        (
            "Android 7 Hashes.pdf",
            "blk0_mmcblk0.bin",
            "SHA1",
            "d5c32aff637c7cf6a0e3132c7e16302b87c8905f",
        ),
        (
            "Android 7 Hashes.pdf",
            "blk0_mmcblk0.bin",
            "SHA256",
            "5a13ae720925e7a8d1367d1cecec1cea5f5ad5753e291887b89e68ae83f49ec7",
        ),
        (
            "Android 7 Hashes.pdf",
            "blk32_mmcblk0rpmb.bin",
            "MD5",
            "a26f0b56848b1bdbb350f70141b58098",
        ),
        (
            "Android 7 Hashes.pdf",
            "blk32_mmcblk0rpmb.bin",
            "SHA1",
            "d24c21c9e7d8fedc072c367d0f6620909c2f91e6",
        ),
        (
            "Android 7 Hashes.pdf",
            "blk32_mmcblk0rpmb.bin",
            "SHA256",
            "b77b5ac1e87dae8050ac63614c22070ab608ac8732fc182f275501050db92ebf",
        ),
        (
            "Android 7 Hashes.pdf",
            "procdata.zip",
            "MD5",
            "7f19ff80cc7faa8643e85dbb6fb08715",
        ),
        (
            "Android 7 Hashes.pdf",
            "procdata.zip",
            "SHA1",
            "6c576f77616d3b8955b9af7fbcfee0f23d9a1298",
        ),
        (
            "Android 7 Hashes.pdf",
            "procdata.zip",
            "SHA256",
            "9d3a582eedfbef8f1572f203d635e318734417f062adfe16fb4adef72ddd9b05",
        ),
        (
            "Android7-ImageCreationDocumentation.pdf",
            "blk0_mmcblk0.bin",
            "MD5",
            "12a9399bc084d024de2c583031cf836a",
        ),
        (
            "Android7-ImageCreationDocumentation.pdf",
            "blk0_mmcblk0.bin",
            "SHA1",
            "b31f1630816535e769d9886719184a3d96decb27",
        ),
        (
            "Android7-ImageCreationDocumentation.pdf",
            "blk0_mmcblk0.bin",
            "SHA256",
            "6fedd6cd7ca05efbf291ca5b12e1c563322f389b6e6e7a2817e817f01ace78d0",
        ),
        (
            "Android7-ImageCreationDocumentation.pdf",
            "blk32_mmcblk0rpmb.bin",
            "MD5",
            "a26f0b56848b1bdbb350f70141b58098",
        ),
        (
            "Android7-ImageCreationDocumentation.pdf",
            "blk32_mmcblk0rpmb.bin",
            "SHA1",
            "d24c21c9e7d8fedc072c367d0f6620909c2f91e6",
        ),
        (
            "Android7-ImageCreationDocumentation.pdf",
            "blk32_mmcblk0rpmb.bin",
            "SHA256",
            "b77b5ac1e87dae8050ac63614c22070ab608ac8732fc182f275501050db92ebf",
        ),
        (
            "Android7-ImageCreationDocumentation.pdf",
            "procdata.zip",
            "MD5",
            "7f19ff80cc7faa8643e85dbb6fb08715",
        ),
        (
            "Android7-ImageCreationDocumentation.pdf",
            "procdata.zip",
            "SHA1",
            "6c576f77616d3b8955b9af7fbcfee0f23d9a1298",
        ),
        (
            "Android7-ImageCreationDocumentation.pdf",
            "procdata.zip",
            "SHA256",
            "9d3a582eedfbef8f1572f203d635e318734417f062adfe16fb4adef72ddd9b05",
        ),
        (
            "LG GSM_H790 Nexus 5X.ufd",
            "blk0_mmcblk0.bin",
            "SHA256",
            "5a13ae720925e7a8d1367d1cecec1cea5f5ad5753e291887b89e68ae83f49ec7",
        ),
        (
            "LG GSM_H790 Nexus 5X.ufd",
            "blk32_mmcblk0rpmb.bin",
            "SHA256",
            "b77b5ac1e87dae8050ac63614c22070ab608ac8732fc182f275501050db92ebf",
        ),
        (
            "LG GSM_H790 Nexus 5X.ufd",
            "procdata.zip",
            "SHA256",
            "9d3a582eedfbef8f1572f203d635e318734417f062adfe16fb4adef72ddd9b05",
        ),
        (
            "blk0_mmcblk0.bin",
            "blk0_mmcblk0.bin",
            "MD5",
            "5dafc6668c2c0e6bb3a928f35676d3bd",
        ),
        (
            "blk0_mmcblk0.bin",
            "blk0_mmcblk0.bin",
            "SHA1",
            "a1412779fe63c84c3ae582976d5f052d7bde5928",
        ),
        (
            "blk0_mmcblk0.bin",
            "blk0_mmcblk0.bin",
            "SHA256",
            "50186bce5071ff82b3e4fed1328a4c200b55b6a49e1acce2e6c0aa79544991c4",
        ),
        (
            "blk0_mmcblk0.bin",
            "blk0_mmcblk0.bin",
            "SHA512",
            "d83a2d90e2b17d8f0b74718d1e6ba8a0549576338d81e304caf8c79b9ea3cb734a56b1ad85594a1566703d258516a8fc427127fa30edcd62550430271a9e51f1",
        ),
        (
            "blk32_mmcblk0rpmb.bin",
            "blk32_mmcblk0rpmb.bin",
            "MD5",
            "a26f0b56848b1bdbb350f70141b58098",
        ),
        (
            "blk32_mmcblk0rpmb.bin",
            "blk32_mmcblk0rpmb.bin",
            "SHA1",
            "d24c21c9e7d8fedc072c367d0f6620909c2f91e6",
        ),
        (
            "blk32_mmcblk0rpmb.bin",
            "blk32_mmcblk0rpmb.bin",
            "SHA256",
            "b77b5ac1e87dae8050ac63614c22070ab608ac8732fc182f275501050db92ebf",
        ),
        (
            "procdata.zip",
            "procdata.zip",
            "MD5",
            "7f19ff80cc7faa8643e85dbb6fb08715",
        ),
        (
            "procdata.zip",
            "procdata.zip",
            "SHA1",
            "6c576f77616d3b8955b9af7fbcfee0f23d9a1298",
        ),
        (
            "procdata.zip",
            "procdata.zip",
            "SHA256",
            "9d3a582eedfbef8f1572f203d635e318734417f062adfe16fb4adef72ddd9b05",
        ),
    }
    computed: Set[Tuple[str, str, str, str]] = set()

    graph = Graph()
    graph.parse("kb.ttl")

    query = """\
SELECT ?lDocumentingFileName ?lHashedFileName ?lHashMethod ?lHashValue
WHERE {
  ?nDocumentingFile
    cito:documents ?nHashingObservation ;
    prov:wasDerivedFrom+ ?nHashingProvenanceRecord ;
    uco-core:hasFacet / uco-observable:fileName ?lDocumentingFileName ;
    .
  ?nHashedFile
    uco-core:hasFacet / uco-observable:fileName ?lHashedFileName ;
    .
  ?nHashingProvenanceRecord
    uco-core:object ?nHashedFile ;
    .
  ?nHashingObservation
    sosa:hasFeatureOfInterest ?nHashedFile ;
    sosa:hasResult ?nHash ;
    uco-action:object ?nHashedFile ;
    uco-action:result ?nHashingProvenanceRecord ;
    .
  ?nHash
    uco-types:hashMethod ?lHashMethod ;
    uco-types:hashValue ?lHashValue ;
    .
}
"""
    for result in graph.query(query):
        assert isinstance(result, ResultRow)
        assert isinstance(result[3], Literal)
        computed.add(
            (
                str(result[0]),
                str(result[1]),
                str(result[2]),
                binascii.hexlify(result[3].toPython()).decode(),
            )
        )
    assert expected == computed


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
        assert isinstance(result, ResultRow)
        assert isinstance(result[0], URIRef)
        hash_iri = str(result[0])
        if RX_UUID.search(hash_iri) is None:
            computed.add(hash_iri)
        else:
            if hash_iri[-22] != "5":
                computed.add(hash_iri)
    assert expected == computed
