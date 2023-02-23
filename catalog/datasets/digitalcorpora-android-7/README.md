<!--
GENERATED FILE

The file README.md is generated from README.md.in and other source files.  Do not edit README.md directly; instead, edit the graph, SPARQL query(/ies), or template README.md.in files in this directory.
-->

# Digital Corpora Android 7

Note: This dataset has some documentation to complete to explain some hashes found from various sources.


## Review of `blk0_mmcblk0.bin`

The file named `blk0_mmcblk0.bin` has several hashes (focusing on SHA-256 for this explanation) recorded in the documentary files.  These hashes are noted with the following "witnessing" files:

| ?lSHA256   | ?nWitnessObject                              | ?lWitnessObjectDescription                               |
|------------|----------------------------------------------|----------------------------------------------------------|
| 50186bc... | kb:file-5aad2637-ebad-46dc-8fdb-58a5078f760a | blk0_mmcblk0.bin, as extracted from distribution tarball |
| 5a13ae7... | kb:file-720a0b83-2de7-466d-99f5-9c4cc458c635 | Android 7 Hashes.pdf                                     |
| 5a13ae7... | kb:file-b0fd0b2d-2412-41f2-a624-b42b8e59ddfe | LG GSM_H790 Nexus 5X.ufd                                 |
| 6fedd6c... | kb:file-2c16fd64-befe-441f-abe4-73a99b4cf154 | Android7-ImageCreationDocumentation.pdf                  |

To understand where changes appear to have occurred in the provenance chain, the following figures illustrate the provenance, including observation and modification activities (typed as [SOSA Observations](https://www.w3.org/TR/vocab-ssn/#SOSAObservation) and [Actuations](https://www.w3.org/TR/vocab-ssn/#SOSAActuation), respectively).

The figures use the PROV-O illustration grammar with `case-prov` adaptations, [documented here](https://github.com/casework/CASE-Implementation-PROV-O#visual-design-notes).  In short, yellow nodes are entities (objects), brown nodes records of those objects, and blue nodes activities.  Also, at the time of this writing, the visual ordering of temporal relationships is not implemented.  Topological ordering gets dependency flow consistent in the up-to-down direction, but placement in the left-right axis is uncontrolled.  Each figure is an SVG, and clicking it will provide a figure with searchable text.

| `blk0_mmcblk0.bin` |  |
| --- | --- |
| Entities | ![Provenance of `blk0_mmcblk0.bin`: entities](filtered-blk0_mmcblk0.bin.entities.svg) |
| Entities and activities | ![Provenance of `blk0_mmcblk0.bin`: entities and activities](filtered-blk0_mmcblk0.bin.activities-entities.svg) |

For comparison, these are the entities-only, and entities-activities illustrations for the other disk image where hashes were consistent across the included records, `blk32_mmcblk0rpmb.bin`.

| `blk32_mmcblk0rpmb.bin` |  |
| --- | --- |
| Entities | ![Provenance of `blk32_mmcblk0rpmb.bin`: entities](filtered-blk32_mmcblk0rpmb.bin.entities.svg) |
| Entities and activities | ![Provenance of `blk32_mmcblk0rpmb.bin`: entities and activities](filtered-blk32_mmcblk0rpmb.bin.activities-entities.svg) |
