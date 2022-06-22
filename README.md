# CASE-Corpora

**(Note: This repository is currently private while undergoing NIST review.)**


## Disclaimer<a id="disclaimer"></a>

Participation by NIST in the creation of the documentation of mentioned software is not intended to imply a recommendation or endorsement by the National Institute of Standards and Technology, nor is it intended to imply that any specific software is necessarily the best available for the purpose.


## Description


### Statements of purpose and maturity

This repository houses a knowledge base graph of publicly available data sets that represent various aspects of cyberspace investigations.  Datasets currently recorded are listed in the [`catalog/`](catalog/#readme) directory.

The primary benefits of the data in this repository are:
* To provide an index of known data sets with downloadable artifacts.
* To provide aggregatable descriptions of public data sets that are not necessarily captured in a machine-readable manner within the dataset artifacts, such as what devices may have been data sources, and what intra-object relationships should be discoverable.  Where possible, from dataset documentation and/or collaboration with dataset authors, ground truth will also be encoded.
* To provide cross-confirmation of chain of custody for dataset artifacts, e.g. so hashes can be confirmed for downloaded artifacts as well as derived artifacts submitted into tools.
* To exercise the expressive abilities of various graph-based ontology languages.

As a project of the [CASE Ontology community](https://caseontology.org/), the primary ontology basis used to annotate data in this repository is CASE.  Because CASE and [UCO](https://unifiedcyberontology.org) do not currently have a focus on representation of datasets, [DCAT 2](https://www.w3.org/TR/vocab-dcat-2/) is used to provide the base structure of a collection of indexes.

This repository provides a "root" entity, a `dcat:Catalog` representing the datasets indexed in CASE-Corpora.  Each dataset known is characterized as a `dcat:Dataset` (or a specialized subclass, `case-corpora:Dataset`, that includes additional integrity checks).  Artifacts within the datasets (such as documentation PDFs and disk images) are each instantiated as a `dcat:Distribution` (similarly, `case-corpora:Distribution`), providing a download URL.  This repository's data set can be "Walked" to look for all download URLs of all distributions within all datasets within the "root" catalog, with this SPARQL query:

```sparql
SELECT ?nDownloadURL
WHERE {
  ?nCatalog
    a dcat:Catalog ;
    dcat:dataset /
      (case-corpora:hasDistribution|dcat:distribution) /
        (case-corpora:hasDownloadURL|dcat:downloadURL) ?nDownloadURL .
}
```

CASE is then used to enrich the knowledge of each `dcat:Distribution`.  A typical distribution file would be a zip, housing files pooled together as a digital forensic training dataset.  CASE is used to characterize these files, and look "backward" and "forward" in their provenance history as they would be used in an investigative workflow.

- *Backward* - From documentation, the provenance of those files back to the data sources (such as an imaged computer) is represented, including reconstructions of investigative actions and times as best attainable from what was described.
- *Forward* - Some files, such as disk images, are extracted and processed up to where they might be used as input to a forensic tool.  An independent analyst reproducing the investigative actions would be able to use these records to cross-verify the hashes since the download action within their chain of custody.

This repository is a community effort.  Contributions are welcome and encouraged, to help the community at large discover what data is available.  Please see [`CONTRIBUTE.md`](CONTRIBUTE.md) if you are interested in contributing.


### Technical installation instructions

This repository is primarily a data repository, and thus has no "Installation" beyond downloading.

All of the datasets' graphs in this repository are aggregated into a "Total knowledge base" file, [`catalog/kb-all.ttl`](catalog/kb-all.ttl).  (A JSON-LD render of this file will be provided in the future.)  This file can be exported to a graph store or queried by itself.

Source code SHACL constraints, and unit tests written in this repository are orchestrated with `make`.  Running `make check` will regenerate aggregation files in the repository, validate content against the used SHACL shapes, and run unit tests.  See [`CONTRIBUTE.md`](contribute.md#Testing) for more details.


## Contact information

[casework/CASE-Corpora](https://github.com/casework/CASE-Corpora/) is developed and maintained by the [case-corpora-maintainers](https://github.com/orgs/casework/teams/case-corpora-maintainers) team and the CASE Adoption Committee.  Please visit [this page](https://caseontology.org/contact.html) if you are interested in joining the committee and/or the CASE community.

Please use [Github Issues](https://github.com/casework/CASE-Corpora/issues) to suggest other data sources, raise concerns, or ask other questions.


## Related Material

* The [CASE-Examples](https://github.com/casework/CASE-Examples/) repository houses other focused CASE illustrations.
* The [CASE website](https://caseontology.org) houses an [examples gallery](https://caseontology.org/examples/) and [description of covered topics](https://caseontology.org/examples/topics.html).


## Cite This Work

Please cite this repository as:

> CASE Community.  *CASE-Corpora* [Data]. Online: <https://github.com/casework/CASE-Corpora> (accessed 2022-04-04).  [https://doi.org/TODO](#TODO)


## Terms of Use

Portions of this repository contributed by NIST are subject to the [NIST Disclaimer of Warranty](LICENSE.md).

Per CASE community practice, software in this repository that is neither contributed by NIST nor imported as a dependency is contributed under the [Apache 2 license](THIRD_PARTY_LICENSES.md).
