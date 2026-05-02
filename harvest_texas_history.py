"""
harvest_texas_history.py
------------------------
Harvests metadata from the Portal to Texas History via OAI-PMH,
cleans it, and saves it as a CSV ready to upload to Hugging Face.

Usage:
    pip install requests
    python harvest_texas_history.py

Output:
    texas_history_collection.csv   — cleaned dataset (~500 records)
    harvest_log.txt                — log of any skipped/error records
"""

import requests
import xml.etree.ElementTree as ET
import csv
import time
import logging
from datetime import datetime

# ── Configuration ────────────────────────────────────────────────────────────

OAI_ENDPOINT = "https://texashistory.unt.edu/oai/"
METADATA_PREFIX = "oai_dc"
TARGET_RECORDS = 500          # How many records to collect
SLEEP_BETWEEN_REQUESTS = 1.5  # Seconds — be polite to the server
OUTPUT_CSV = "texas_history_collection.csv"
LOG_FILE = "harvest_log.txt"

# Dublin Core namespace
DC_NS = "http://purl.org/dc/elements/1.1/"
OAI_DC_NS = "http://www.openarchives.org/OAI/2.0/oai_dc/"
OAI_NS = "http://www.openarchives.org/OAI/2.0/"

# ── Logging setup ─────────────────────────────────────────────────────────────

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)
log = logging.getLogger()

# ── Helpers ───────────────────────────────────────────────────────────────────

def get_text(element, tag, ns):
    """Extract text from first matching child element."""
    found = element.find(f"{{{ns}}}{tag}")
    return found.text.strip() if found is not None and found.text else ""

def get_all_text(element, tag, ns):
    """Extract text from ALL matching child elements, joined by ' | '."""
    found = element.findall(f"{{{ns}}}{tag}")
    values = [e.text.strip() for e in found if e.text and e.text.strip()]
    return " | ".join(values)

def clean_text(text):
    """Basic text cleaning — collapse whitespace, strip control chars."""
    if not text:
        return ""
    return " ".join(text.split())

def parse_record(record_elem):
    """
    Parse a single <record> OAI-PMH element into a flat dict.
    Returns None if the record should be skipped.
    """
    # Skip deleted records
    header = record_elem.find(f"{{{OAI_NS}}}header")
    if header is not None and header.get("status") == "deleted":
        return None

    # Get OAI identifier
    identifier_elem = header.find(f"{{{OAI_NS}}}identifier") if header is not None else None
    oai_id = identifier_elem.text.strip() if identifier_elem is not None and identifier_elem.text else ""

    # Navigate to dc metadata
    metadata = record_elem.find(f"{{{OAI_NS}}}metadata")
    if metadata is None:
        log.warning(f"No metadata found for record {oai_id}")
        return None

    dc = metadata.find(f"{{{OAI_DC_NS}}}dc")
    if dc is None:
        log.warning(f"No dc element found for record {oai_id}")
        return None

    title       = clean_text(get_text(dc, "title", DC_NS))
    description = clean_text(get_text(dc, "description", DC_NS))
    subject     = clean_text(get_all_text(dc, "subject", DC_NS))
    creator     = clean_text(get_all_text(dc, "creator", DC_NS))
    date        = clean_text(get_text(dc, "date", DC_NS))
    type_       = clean_text(get_all_text(dc, "type", DC_NS))
    format_     = clean_text(get_text(dc, "format", DC_NS))
    language    = clean_text(get_text(dc, "language", DC_NS))
    publisher   = clean_text(get_text(dc, "publisher", DC_NS))
    rights      = clean_text(get_text(dc, "rights", DC_NS))
    source      = clean_text(get_text(dc, "source", DC_NS))
    relation    = clean_text(get_all_text(dc, "relation", DC_NS))
    coverage    = clean_text(get_all_text(dc, "coverage", DC_NS))

    # Build the portal URL from the OAI identifier
    # OAI IDs look like: oai:texashistory.unt.edu:metapth12345
    portal_url = ""
    if "texashistory.unt.edu:" in oai_id:
        ark = oai_id.split("texashistory.unt.edu:")[-1]
        portal_url = f"https://texashistory.unt.edu/{ark}/"

    return {
        "oai_id":       oai_id,
        "title":        title,
        "description":  description,
        "subject":      subject,
        "creator":      creator,
        "date":         date,
        "type":         type_,
        "format":       format_,
        "language":     language,
        "publisher":    publisher,
        "rights":       rights,
        "source":       source,
        "relation":     relation,
        "coverage":     coverage,
        "portal_url":   portal_url,
    }

def is_usable(record):
    """
    Quality filter — only keep records with at least a title and description.
    Adjust this threshold as needed.
    """
    return bool(record.get("title")) and bool(record.get("description"))

# ── Main harvest loop ─────────────────────────────────────────────────────────

def harvest(target=TARGET_RECORDS):
    records = []
    resumption_token = None
    page = 0
    skipped = 0

    print(f"Starting harvest from {OAI_ENDPOINT}")
    print(f"Target: {target} usable records\n")

    while len(records) < target:
        page += 1

        # Build request URL
        if resumption_token:
            params = {
                "verb": "ListRecords",
                "resumptionToken": resumption_token
            }
        else:
            params = {
                "verb": "ListRecords",
                "metadataPrefix": METADATA_PREFIX,
            }

        print(f"  Fetching page {page} (collected {len(records)}/{target})...")
        log.info(f"Fetching page {page}, resumptionToken={resumption_token}")

        try:
            response = requests.get(OAI_ENDPOINT, params=params, timeout=30)
            response.raise_for_status()
        except requests.RequestException as e:
            log.error(f"Request failed on page {page}: {e}")
            print(f"  ⚠ Request failed: {e}. Retrying in 5s...")
            time.sleep(5)
            continue

        # Parse XML
        try:
            root = ET.fromstring(response.content)
        except ET.ParseError as e:
            log.error(f"XML parse error on page {page}: {e}")
            print(f"  ⚠ XML parse error: {e}")
            break

        # Check for OAI errors
        error_elem = root.find(f"{{{OAI_NS}}}error")
        if error_elem is not None:
            print(f"  ✗ OAI error: {error_elem.get('code')} — {error_elem.text}")
            log.error(f"OAI error: {error_elem.get('code')} — {error_elem.text}")
            break

        # Extract records
        list_records = root.find(f"{{{OAI_NS}}}ListRecords")
        if list_records is None:
            print("  ✗ No ListRecords element found.")
            break

        for record_elem in list_records.findall(f"{{{OAI_NS}}}record"):
            parsed = parse_record(record_elem)
            if parsed is None:
                skipped += 1
                continue
            if not is_usable(parsed):
                skipped += 1
                log.info(f"Skipped (missing title/description): {parsed.get('oai_id')}")
                continue
            records.append(parsed)
            if len(records) >= target:
                break

        # Check for resumption token
        token_elem = list_records.find(f"{{{OAI_NS}}}resumptionToken")
        if token_elem is not None and token_elem.text and token_elem.text.strip():
            resumption_token = token_elem.text.strip()
        else:
            print("\n  ✓ No more pages — harvest complete.")
            break

        time.sleep(SLEEP_BETWEEN_REQUESTS)

    print(f"\nHarvest done: {len(records)} usable records, {skipped} skipped.")
    log.info(f"Harvest complete: {len(records)} records, {skipped} skipped.")
    return records

# ── Write CSV ─────────────────────────────────────────────────────────────────

def save_csv(records, path=OUTPUT_CSV):
    if not records:
        print("No records to save.")
        return

    fieldnames = [
        "oai_id", "title", "description", "subject", "creator",
        "date", "type", "format", "language", "publisher",
        "rights", "source", "relation", "coverage", "portal_url"
    ]

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"Saved {len(records)} records to {path}")
    log.info(f"Saved CSV: {path}")

# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    start = datetime.now()
    records = harvest(target=TARGET_RECORDS)
    save_csv(records)
    elapsed = (datetime.now() - start).seconds
    print(f"\nTotal time: {elapsed}s")
    print(f"Log written to: {LOG_FILE}")
    print(f"\nNext step: upload {OUTPUT_CSV} to Hugging Face as a dataset!")
