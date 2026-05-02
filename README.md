# Texas History Semantic Search

An end-to-end AI/ML project for library digital collections — from raw metadata harvesting to a live semantic search application.

Built as an AI/ML project demonstrating the intersection of library science and machine learning, with a focus on Texas historical collections.

🔗 [**Try the live app on Hugging Face**](https://huggingface.co/spaces/AngelaColmen/texas-history-semantic-search)  
📦 [**View the dataset on Hugging Face**](https://huggingface.co/datasets/AngelaColmen/texas-history-collection)

\---

## What It Does

This app lets users search 500+ Texas historical records by **meaning**, not just keywords. A user can type something like *"early farming communities along the Rio Grande"* and get relevant results even if those exact words don't appear in any record.

Each result shows the title, date, format, subject headings, a description excerpt, and a direct link to the full record on the Portal to Texas History.

\---

## Project Pipeline

```
Portal to Texas History (OAI-PMH)
        ↓
harvest\_texas\_history.py       — harvests \& cleans 500 metadata records
        ↓
texas\_history\_collection.csv   — structured dataset published on Hugging Face
        ↓
app.py                         — Gradio semantic search app built on the dataset
        ↓
Live Space on Hugging Face
```

\---

## Files

|File|Description|
|-|-|
|`harvest\_texas\_history.py`|Harvests metadata from the Portal to Texas History via OAI-PMH and saves a clean CSV|
|`fix\_portal\_urls.py`|Utility script that builds direct Portal URLs from OAI identifier fields|
|`texas\_history\_collection.csv`|The curated dataset of 500 records|
|`dataset\_README.md`|Hugging Face dataset card with full documentation of schema, provenance, and intended uses|
|`app.py`|Gradio application for semantic search over the dataset|

\---

## Technologies Used

* **OAI-PMH** — Open Archives Initiative Protocol for Metadata Harvesting
* **Dublin Core** — metadata standard used by the Portal to Texas History
* **sentence-transformers** — `all-MiniLM-L6-v2` model for semantic embeddings
* **Gradio** — web interface framework for the search app
* **Hugging Face** — dataset hosting and app deployment
* **pandas** — data cleaning and manipulation

\---

## Library Science Context

This project applies core library science concepts to AI/ML workflows:

* **Metadata standards** — Dublin Core fields (title, description, subject, creator, date, type) structure the dataset
* **Controlled vocabulary** — subject headings from the Portal to Texas History are preserved and displayed as searchable tags
* **Provenance documentation** — the dataset card documents where the data came from, how it was collected, and its limitations
* **Rights management** — CC0 license applied; original object rights respected by linking back to the source
* **OAI-PMH** — standard protocol used by libraries, archives, and repositories for metadata interchange

\---

## How to Run Locally

```bash
# Install dependencies
pip install requests pandas sentence-transformers gradio torch

# Harvest the dataset
python harvest\_texas\_history.py

# Fix portal URLs
python fix\_portal\_urls.py

# Run the app
python app.py
```

\---

## Author

**Angela Colmenares**  
[Hugging Face](https://huggingface.co/AngelaColmen) · [LinkedIn](https://www.linkedin.com/in/angelacolmen) · [GitHub](https://github.com/AngelaColmen)

\---

*Data sourced from the* [*Portal to Texas History*](https://texashistory.unt.edu/)*, maintained by the University of North Texas Libraries. Dataset licensed CC0.*

