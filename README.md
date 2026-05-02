# Texas History Semantic Search

An AI-powered semantic search application for exploring historical records from the [Portal to Texas History](https://texashistory.unt.edu/). Built to demonstrate how embedding models can enhance discovery in digital special collections.

## Overview

This application enables meaning-based search across 500+ digitized historical records, moving beyond keyword matching to surface conceptually relevant results. A user searching for *"early settler communities along the Rio Grande"* will retrieve records that are thematically related — even when the exact words do not appear in the metadata.

Developed as part of an exploration into AI applications for library and archival discovery systems.

## Features

- Semantic search powered by the [GTE-Large](https://huggingface.co/thenlper/gte-large) embedding model
- Dataset harvested from the Portal to Texas History via OAI-PMH
- TAMU-branded interface built with Gradio
- Results include metadata, subject tags, match scores, and direct links to archival records

## Embedding Model

This project uses **GTE-Large** (General Text Embeddings, Large) by Alibaba DAMO Academy. GTE-Large was selected over general-purpose sentence embedding models for its stronger performance on dense, descriptive academic and archival text. It is fully open source under the MIT license.

| Model | Size | Best For |
|---|---|---|
| all-MiniLM-L6-v2 (previous) | 90MB | General purpose |
| GTE-Large (current) | 670MB | Academic and historical text |

## Tech Stack

- `sentence-transformers` — embedding and semantic search
- `gradio` — user interface
- `pandas` — data handling
- `torch` — model inference
- Dataset hosted on [Hugging Face Datasets](https://huggingface.co/datasets/AngelaColmen/texas-history-collection)

## Live Demo

Try the app on [Hugging Face Spaces](https://huggingface.co/AngelaColmen).

## About

Built by Angela Colmenares, AI Librarian. This project sits at the intersection of information science and applied machine learning, exploring how modern embedding models can expand access to cultural heritage collections.

## Rights and Permissions

This dataset contains bibliographic metadata harvested from the Portal to Texas History (https://texashistory.unt.edu/), maintained by the University of North Texas Libraries. The metadata fields (title, description, subject headings, etc.) are factual in nature and are made available here under a CC0 1.0 license.

However, **rights to the underlying digital objects vary by record and by contributing institution**. Some materials are in the public domain; others may be under copyright or have restricted use conditions. The `rights` field in each record reflects the rights statement provided by the contributing institution, where available.

Users who wish to reproduce, publish, or reuse the underlying digital objects (images, documents, etc.) should:
- Consult the `rights` field for each individual record
- Follow the link in `portal_url` to review the full rights statement on the Portal to Texas History
- Contact the holding institution directly if the intended use is unclear

This project does not claim ownership of any underlying digital objects and does not reproduce them. All links point back to the original records at the Portal to Texas History.

## About
 
Built by Angela Colmenares, AI Librarian. This project sits at the intersection of information science and applied machine learning, exploring how modern embedding models can expand access to cultural heritage collections.

\---

*Data sourced from the* [*Portal to Texas History*](https://texashistory.unt.edu/)*, maintained by the University of North Texas Libraries. Dataset licensed CC0.*

