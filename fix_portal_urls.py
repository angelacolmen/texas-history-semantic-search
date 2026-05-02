"""
fix_portal_urls.py
------------------
Reads texas_history_collection.csv, builds proper Portal to Texas History
URLs from the oai_id field, and saves a corrected version.

Usage:
    python fix_portal_urls.py

Input:  texas_history_collection.csv  (in the same folder)
Output: texas_history_collection_fixed.csv
"""

import pandas as pd

INPUT_FILE  = "texas_history_collection.csv"
OUTPUT_FILE = "texas_history_collection_fixed.csv"

# Load CSV
print(f"Loading {INPUT_FILE}...")
df = pd.read_csv(INPUT_FILE)
print(f"Loaded {len(df)} records.")

# Build portal URLs from oai_id
# oai_id looks like: info:ark/67531/metapth2355
# URL should be:     https://texashistory.unt.edu/ark:/67531/metapth2355/

def build_url(oai_id):
    if not isinstance(oai_id, str) or not oai_id.strip():
        return ""
    # Extract everything after "info:ark/"
    if "ark/" in oai_id:
        ark_path = oai_id.split("ark/")[-1].strip()
        return f"https://texashistory.unt.edu/ark:/{ark_path}/"
    return ""

df["portal_url"] = df["oai_id"].apply(build_url)

# Report results
filled = df["portal_url"].astype(bool).sum()
empty  = len(df) - filled
print(f"URLs built: {filled} filled, {empty} still empty.")

# Show a few examples
print("\nSample URLs:")
for _, row in df[df["portal_url"] != ""].head(3).iterrows():
    print(f"  {row['oai_id']}")
    print(f"  -> {row['portal_url']}")
    print()

# Save fixed CSV
df.to_csv(OUTPUT_FILE, index=False)
print(f"Saved fixed CSV to: {OUTPUT_FILE}")
print("\nNext steps:")
print("  1. Check a few URLs in your browser to make sure they work")
print("  2. Upload texas_history_collection_fixed.csv to your Hugging Face dataset")
print("  3. Replace the old texas_history_collection.csv with this fixed version")
