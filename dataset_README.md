---
language:
- en
license: cc0-1.0
tags:
- library-science
- digital-humanities
- metadata
- texas-history
- cultural-heritage
- oai-pmh
- dublin-core
pretty_name: Texas History Collection – Portal Metadata
size_categories:
- 100<n<1K
task_categories:
- text-classification
- feature-extraction
- text-retrieval
---

# Texas History Collection – Portal Metadata

A curated dataset of bibliographic metadata records harvested from the
[Portal to Texas History](https://texashistory.unt.edu/), maintained by the
University of North Texas Libraries. The Portal aggregates rare, historical,
and primary source materials from or about Texas, and serves as a service hub
for the Digital Public Library of America (DPLA).

This dataset was created to support AI/ML experimentation in library and
digital collections contexts, including semantic search, subject heading
recommendation, and metadata enrichment tasks.

---

## Dataset Details

### Dataset Description

- **Curated by:** Angela Colmenares
- **Language:** English
- **License:** [CC0 1.0 Universal (Public Domain)](https://creativecommons.org/publicdomain/zero/1.0/)
- **Source:** Portal to Texas History OAI-PMH feed (`oai_dc` format)
- **Harvest date:** 2025

### Source Data

Metadata was harvested via the OAI-PMH protocol from:

```
https://texashistory.unt.edu/oai/?verb=ListRecords&metadataPrefix=oai_dc
```

Records are encoded using [Dublin Core](https://www.dublincore.org/specifications/dublin-core/dces/)
(`oai_dc`), the standard metadata schema for OAI-PMH interchange.

Only records with both a `title` and a `description` field were retained.
Deleted records (as flagged by the OAI-PMH feed) were excluded.

---

## Schema

Each record contains the following fields:

| Field        | Description                                                       | Example                              |
|--------------|-------------------------------------------------------------------|--------------------------------------|
| `oai_id`     | OAI-PMH identifier for the record                                 | `oai:texashistory.unt.edu:metapth123`|
| `title`      | Title of the item                                                 | `Map of Texas, 1836`                 |
| `description`| Textual description or abstract                                   | `An early cartographic representation...` |
| `subject`    | Subject headings, pipe-separated if multiple                      | `Texas--History \| Maps`              |
| `creator`    | Author(s) or creator(s), pipe-separated if multiple               | `Austin, Stephen F.`                 |
| `date`       | Date of creation or publication                                   | `1836`                               |
| `type`       | Type of resource (image, text, sound, etc.)                       | `Image`                              |
| `format`     | File format or physical medium                                    | `image/jpeg`                         |
| `language`   | Language of the resource                                          | `en`                                 |
| `publisher`  | Publisher or holding institution                                  | `Dolph Briscoe Center for American History` |
| `rights`     | Rights statement                                                  | `Public Domain`                      |
| `source`     | Source collection or parent resource                              | `Texas State Library and Archives`   |
| `relation`   | Related resources, pipe-separated if multiple                     | `https://texashistory.unt.edu/...`   |
| `coverage`   | Spatial or temporal coverage, pipe-separated                      | `Texas \| 1836`                       |
| `portal_url` | Direct URL to the item on the Portal to Texas History             | `https://texashistory.unt.edu/...`   |

---

## Intended Uses

### Direct Use
- **Semantic search demos** — encode `description` fields with sentence transformers to enable meaning-based retrieval
- **Subject heading recommendation** — train or prompt models to suggest subjects from title + description
- **Metadata quality analysis** — explore completeness, coverage, and consistency across fields
- **Digital humanities research** — study the composition of Texas historical collections

### Out-of-Scope Use
- This dataset should not be used to train models that would reproduce or replace the Portal to Texas History or its partners' services
- Commercial use of the underlying digital objects should be verified against the rights statements in each record

---

## Dataset Creation

### Curation Rationale

Library metadata is an underrepresented domain in publicly available NLP/ML datasets.
This dataset aims to fill that gap for Texas and regional history collections,
supporting both practical library AI tools and broader digital humanities research.

### Source Data Collection

Records were harvested using the OAI-PMH `ListRecords` verb with the `oai_dc`
metadata prefix. Pagination was handled via OAI-PMH resumption tokens. A 1.5-second
delay was observed between requests to be respectful of the server.

### Filtering

Records were included only if they contained non-empty `title` and `description`
fields. Deleted records (OAI-PMH status="deleted") were excluded.

---

## Bias and Limitations

- Coverage reflects what Portal partners have digitized and made available — this is not a complete or representative sample of Texas history
- Descriptions vary significantly in length and quality across partner institutions
- Subject headings may use legacy or non-standardized terminology
- Date formats are inconsistent across records (some are year-only, some include month/day)

---

## Citation

If you use this dataset, please cite the Portal to Texas History:

```
Portal to Texas History. University of North Texas Libraries.
https://texashistory.unt.edu/
```

---

## Contact

Angela Colmenares — [HuggingFace](https://huggingface.co/AngelaColmen) · [LinkedIn](https://www.linkedin.com/in/angelacolmen) · [GitHub](https://github.com/AngelaColmen)
