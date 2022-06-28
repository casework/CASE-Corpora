# Contributing to CASE-Corpora

Assistance is welcome in many ways on this project, as it is intended to be a community-curated resource.


## Contribution of new datasets

CASE-Corpora makes certain requirements of new dataset contributions.  These requirements are drawn from "Upstream" ontologies, particularly [DCAT-US](https://resources.data.gov/resources/dcat-us/) and [CASE](https://caseontology.org/).  The minimal requirements are outlined in the "New Dataset Entry" form when submitting a new Github Issue, but explained further here.

First, the submitted or suggested `dcat:Dataset` record must have the property [`pod:accessLevel`](https://resources.data.gov/resources/dcat-us/#accessLevel) populated.  The preferred value is `"public"`, as community members can contribute extension annotations to these indexed datasets.  Repository maintainers will classify these as `case-corpora:Dataset`s, which are `dcat:Dataset`s with some mechanisms to tie in CASE annotations and requirements.  Non-public datasets may also be accepted, and will be instantiated as `dcat:Dataset`s.


### Contributing minimal data for new datasets

SHACL shapes are provided to confirm when minimal requirements are met for the generated data, and are tested as part of CI before pull requests are accepted into the `main` branch.  People interested in contributing a yet-unlisted dataset to the index do not need to write the data themselves, but it is certainly a welcome contribution.  The Github Issues template requests the minimal data needed to get a `Dataset` started, and this can be provided in free-form text.


### Files made for each dataset

(Note that the files below can be found as either Turtle (`.ttl`) or JSON-LD (`.json`, `.jsonld`), as was convenient for the data drafter.)

The graph source files share a name scheme separating data that is *minimally viable*; from supplemental and manually maintained; from ground truth, also manually maintained; from generated:

* `dataset.ttl` - This file stores the minimal `Dataset` definition required by DCAT-US.
* `distribution.ttl` - This file stores the minimal `Distribution` definitions required by CASE-Corpora.  For non-public datasets, this file might be absent.  For public datasets, at least one `case-corpora:Distribution` must be provided, and each `Distribution` must have a `dcat:downloadURL` statement (preferring a `case-corpora:hasDownloadURL` spelling).
* `supplemental.ttl` - This file stores non-minimal, hand-maintained extension information about the dataset, such as cyber-relevant items that the distributions were derived from, personas and organizations used in the data set, actions expected to be known to have occurred within the dataset, and more.  Data within `supplemental.ttl` should be drawn from "Starting point" documentation for the scenario.  However, data that amount to investigative conclusions should be stored in `ground-truth.ttl`.
* `generated-*.ttl` - These files contain automatically-derived RDF content according to some recipe that takes the above files as input, such as the [CASE mapping to PROV-O](https://github.com/casework/CASE-Implementation-PROV-O).  Maintainers won't be editing these files by hand, but workflow needs might need to run some generating script to refresh them after manual updates to other files.
* `ground-truth.ttl` - This file stores known answers one should find from analysis of the dataset.  For instance, the ["2010-nps-emails"](https://digitalcorpora.org/archives/173) disk image documentation notes that an email address `plain_text@textedit.com` is stored within some file in the disk, and the file was created with Apple TextEdit.  `ObservableAction`s and `ObservableRelationship`s would be recorded in `ground-truth.ttl` to indicate this.  The `uco-observable:Application` and `uco-observable:EmailAddress` objects should be defined in `supplemental.ttl`, but their `Action`s and `Relationship`s should be defined in `ground-truth.ttl`. 
* `generated-ground-truth-*.ttl` - These files include `ground-truth.ttl` in their generation, and subtract the contents of the associated generated file.

For the files above, `dataset.ttl` and `distribution.ttl` have requirements on their content specific to CASE-Corpora.  Otherwise, content within the files is validated according to available ontology and SHACL resources.  All supplemental data are populated according to community interest.


### Alternative download references

If a `dcat:downloadURL` references an address that is no longer available, an alternative download location should be provided, and hashes of that alternative resource should be computed and recorded.  These will be encoded with CASE records, and linked to the original resources using [`prov:alternateOf`](https://www.w3.org/TR/prov-o/#alternateOf).


## Extending dataset descriptions


### Excerpting source text

When excerpting original text from documentation, e.g. for the `dcterms:description` of the `dcat:Dataset`, please use quotation marks.


### References of identities


#### References of real people

When referencing a real person, it is acceptable as a matter of pooling authorship and publication metadata to take person names and email addresses *exactly as they are presented in dataset documentation*.  Graph identifiers for people may be shared between datasets when documented names and emails match.  To do any further graph linking of a person (e.g., to an [ORCID](https://orcid.org/), or if the person is known to have changed institutions and/or email addresses), that person must provide consent on a Github Issue or Pull Request.

When a submitted dataset might contain human---that is, real person---data, the dataset provider must attest that they have permission and appropriate consent to share a person's data.  The consent could be a photo release, privacy consent, research informed consent -- whatever is appropriate for the situation.

This repository uses this definition of "human subject", from [45 CFR 46.102(e)(1)](https://www.hhs.gov/ohrp/regulations-and-policy/regulations/45-cfr-46/revised-common-rule-regulatory-text/index.html):

> *Human subject* means a living individual about whom an investigator (whether professional or student) conducting research:
>
> (i) Obtains information or biospecimens through intervention or interaction with the individual, and uses, studies, or analyzes the information or biospecimens; or
>
> (ii) Obtains, uses, studies, analyzes, or generates identifiable private information or identifiable biospecimens.


##### References of points of contact

DCAT-US [requires](https://resources.data.gov/resources/dcat-us/#contactPoint) a point of contact be specified for any `dcat:Dataset`.  Unfortunately, this is frequently unavailable.  If a `dcat:Dataset`'s point of contact is not publicy documented, use CASE-Corpora's "null" contact, `case-corpora:contact-00000000-0000-0000-0000-000000000000`.


#### References of real organizations

When referencing a real organization (e.g. for `dcterms:publisher`), CASE-Corpora chooses to use Wikidata entries as their IRI, if they have one.  For example, the US National Institute of Standards and Technology has this IRI as a WikiData entity:

[`http://www.wikidata.org/entity/Q176691`](http://www.wikidata.org/entity/Q176691)

This IRI is used in CASE-Corpora with the prefix `wd`, appearing as `wd:Q176691`.

If a WikiData IRI does not exist, please define the organization IRI as a general CASE-Corpora knowledge base member in [`catalog/shared/dcat-minimal.ttl`](catalog/shared/dcat-minimal.ttl) so other datasets may reuse it.

*Usage of Wikidata is not a normative practice or requirement of the CASE community, and is only selected as a demonstration of usage of externally-maintained identifiers.  See also the general [disclaimer](README.md#disclaimer).*



### Ground truth updates

Any updates to the ground truth should be sourced from either:

1. Documentation accompanying the dataset, authored by the dataset developer, and not access-protected.  (For instance, some of the Digital Corpora scenarios contain password-protected "Teachers' guides" with answer keys.  CASE-Corpora will not represent these in the publicly visible graph.)
2. The dataset author themselves.

Note that there is a distinction CASE-Corpora maintains between *investigative conclusions* and *ground truth*.  For instance, documentation from the author might denote a certain action concluded at `2018-01-01T19:00Z`, based on a minute-precision clock they monitored at the time of data set generation.  One or more analyses might come to the conclusion that the action described in the ground truth concluded at `2018-01-01T19:00:12.3456Z`.  These do not warrant revisions to the ground truth, as the more precise time stamp is a result of an investigative process, even if that process is repeated with consistent conclusion to the microsecond by multiple independent analysts.

The CASE-Corpora maintainers look forward to discussions framing when conclusions are consistent or inconsistent with ground truth.


## Enrichments

Each of the following enrichments is optional, but enhances the quality and utility of the data annotations.


### CASE Chain of Custody

It is helpful for the "beginning" of a chain of custody to be defined for datasets that represent cyber investigation scenarios.  The beginning includes:

* Defining a [`Investigation`](https://ontology.caseontology.org/case/investigation/Investigation) object;
* Defining the initial [`InvestigativeAction`s](https://ontology.caseontology.org/case/investigation/InvestigativeAction) that introduce evidence into the chain of custody;
* Writing a chain of other `InvestigativeAction`s that lead through the generation of the `Distribution` object one would download;
* Writing a chain of `InvestigativeAction`s one might take to take the `Distribution` and convert its output into a form a forensic tool might recognize.

At the least, the objective of CASE-Corpora is to increase access and discoverability of reference data.  Hence, enrichments seek to at least reach support of these checksum verifications:

* *What is the hash of the thing one would download to try this scenario?*
* *What is the hash of the file one would use as input for some forensic tool or analysis?*


#### Example 1

Suppose a distribution `kb:distribution-aa009e08-67d7-4166-b37b-ab413d300d59` is delivered as one Zip file, downloadable from `http://datasets.example.org/dataset-1.zip`, and the dataset authors note that the Zip file's hashes are an MD5 of `bfe1b0ea5748a664962389e296fc4448` and SHA-1 of `3801819f1a15bf6235f0e600f6c03590f1979f72`.

There are two nodes that CASE-Corpora would characterize from this documentation.

`distribution.json` would contain the following, to describe the `Distribution`:

```json
{
    "@context": {
        "case-corpora": "http://example.org/ontology/case/corpora/",
        "dcat": "http://www.w3.org/ns/dcat#",
        "kb": "http://example.org/kb/",
        "mime": "http://www.iana.org/assignments/media-types/",
        "uco-observable": "https://ontology.unifiedcyberontology.org/uco/observable/",
    },
    "@graph": [
        {
            "@id": "kb:distribution-aa009e08-67d7-4166-b37b-ab413d300d59",
            "@type": "case-corpora:Distribution",
            "case-corpora:hasDownloadURL": {
                "@id": "http://datasets.example.org/dataset-1.zip"
            },
            "dcat:mediaType": {
                "@id": "mime:application/zip"
            }
        },
        {
            "@id": "http://datasets.example.org/dataset-1.zip",
            "@type": "uco-observable:URL"
        }
    ]
}
```

`supplmental.json` would contain the following, to further describe the resource retrievable from the download URL:

```json
{
    "@context": {
        "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
        "uco-observable": "https://ontology.unifiedcyberontology.org/uco/observable/",
        "uco-types": "https://ontology.unifiedcyberontology.org/uco/types/",
        "uco-vocabulary": "https://ontology.unifiedcyberontology.org/uco/vocabulary/",
        "xsd": "http://www.w3.org/2001/XMLSchema#"
    },
    "@graph": [
        {
            "@id": "kb:distribution-aa009e08-67d7-4166-b37b-ab413d300d59",
            "@type": "uco-observable:ArchiveFile",
            "uco-core:hasFacet": [
                {
                    "@type": "uco-observable:ContentDataFacet",
                    "uco-observable:dataPayloadReferenceURL": {
                        "@id": "http://datasets.example.org/dataset-1.zip"
                    },
                    "uco-observable:hash": [
                        {
                            "@type": "uco-types:Hash",
                            "uco-types:hashMethod": {
                                "@type": "uco-vocabulary:HashNameVocab",
                                "@value": "MD5"
                            },
                            "uco-types:hashValue": {
                                "@type": "xsd:hexBinary",
                                "@value": "bfe1b0ea5748a664962389e296fc4448"
                            }
                        },
                        {
                            "@type": "uco-types:Hash",
                            "uco-types:hashMethod": {
                                "@type": "uco-vocabulary:HashNameVocab",
                                "@value": "SHA1"
                            },
                            "uco-types:hashValue": {
                                "@type": "xsd:hexBinary",
                                "@value": "3801819f1a15bf6235f0e600f6c03590f1979f72"
                            }
                        }
                    ],
                    "uco-observable:mimeType": "application/zip"
                },
                {
                    "@type": "uco-observable:FileFacet",
                    "uco-observable:fileName": "dataset-1.zip"
                }
            ]
        },
        {
            "@id": "http://datasets.example.org/dataset-1.zip",
            "uco-core:hasFacet": {
                "@type": "uco-observable:URLFacet",
                "uco-observable:fullValue": "http://datasets.example.org/dataset-1.zip",
                "uco-observable:scheme": "http"
            }
        }
    ]
}
```

An interested user might submit that they've made a mirror of this file, to bypass usage of the HTTP scheme and also supply a stronger hash to verify, a SHA2-256 of `f3aa30bb627d907c16cf6b04aa9fdc27aba4d9f7636e14cae11e6dfc6204874a`.  (Several potential motivations exist for them doing so, such as the dataset's distribution server might not support HTTPS distribution; or, the dataset might have been found from an old source, and may have already been mirrored by a third party.)

The interested user reports their mirrored copy is at `https://mirrors.example.net/dataset-1.zip`.  CASE-Corpora uses [`prov:alternateOf`](https://www.w3.org/TR/prov-o/#alternateOf) in this scenario, linking the mirrored file and mirroring URL to the originals.

```json
{
    "@context": {
        "prov": "http://www.w3.org/ns/prov#",
        "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
        "uco-observable": "https://ontology.unifiedcyberontology.org/uco/observable/",
        "uco-types": "https://ontology.unifiedcyberontology.org/uco/types/",
        "uco-vocabulary": "https://ontology.unifiedcyberontology.org/uco/vocabulary/",
        "xsd": "http://www.w3.org/2001/XMLSchema#"
    },
    "@graph": [
        {
            "@id": "kb:file-53565efd-40e2-4d4a-a459-9e2bbdf35e08",
            "@type": "uco-observable:ArchiveFile",
            "prov:alternateOf": {
                "@id": "kb:distribution-aa009e08-67d7-4166-b37b-ab413d300d59",
            },
            "prov:wasDerivedFrom": {
                "@id": "kb:distribution-aa009e08-67d7-4166-b37b-ab413d300d59",
            },
            "uco-core:hasFacet": [
                {
                    "@type": "uco-observable:ContentDataFacet",
                    "uco-observable:dataPayloadReferenceURL": {
                        "@id": "https://mirrors.example.net/dataset-1.zip"
                    },
                    "uco-observable:hash": [
                        {
                            "@type": "uco-types:Hash",
                            "uco-types:hashMethod": {
                                "@type": "uco-vocabulary:HashNameVocab",
                                "@value": "MD5"
                            },
                            "uco-types:hashValue": {
                                "@type": "xsd:hexBinary",
                                "@value": "bfe1b0ea5748a664962389e296fc4448"
                            }
                        },
                        {
                            "@type": "uco-types:Hash",
                            "uco-types:hashMethod": {
                                "@type": "uco-vocabulary:HashNameVocab",
                                "@value": "SHA1"
                            },
                            "uco-types:hashValue": {
                                "@type": "xsd:hexBinary",
                                "@value": "3801819f1a15bf6235f0e600f6c03590f1979f72"
                            }
                        },
                        {
                            "@type": "uco-types:Hash",
                            "uco-types:hashMethod": {
                                "@type": "uco-vocabulary:HashNameVocab",
                                "@value": "SHA256"
                            },
                            "uco-types:hashValue": {
                                "@type": "xsd:hexBinary",
                                "@value": "f3aa30bb627d907c16cf6b04aa9fdc27aba4d9f7636e14cae11e6dfc6204874a"
                            }
                        }
                    ],
                    "uco-observable:mimeType": "application/zip"
                },
                {
                    "@type": "uco-observable:FileFacet",
                    "uco-observable:fileName": "dataset-1.zip"
                }
            ]
        },
        {
            "@id": "https://mirrors.example.net/dataset-1.zip",
            "@type": "uco-observable:URL",
            "prov:alternateOf": {
                "@id": "kb:distribution-aa009e08-67d7-4166-b37b-ab413d300d59",
            },
            "uco-core:hasFacet": {
                "@type": "uco-observable:URLFacet",
                "uco-observable:fullValue": "https://mirrors.example.net/dataset-1.zip",
                "uco-observable:scheme": "https"
            }
        }
    ]
}
```


### Taxonomic expansion

CASE-Corpora also serves as an opportunity to discover when known taxons are used in datasets.  For instance, a taxonomy of devices can be referenced when a dataset uses one of its members, like an Internet of Things (IoT) device or other specialized sensor.  Or, IANA media type usage can be aggregated.  The [`reports`](reports/) directory provides reports of the used taxons.

CASE-Corpora can also serve as an incubation point for other UCO-maintained taxonomies.  The [`taxonomy`](taxonomy/) directory houses initial drafts of taxonomy members, to serve immediate dataset needs.  Those taxons can be transferred to other taxonomies after "incubating" here.
