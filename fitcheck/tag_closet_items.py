import os
import json
from tagging import tag_closet_item

# Define folders
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CLOSET_DIR = os.path.join(BASE_DIR, "Closet")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "inventory.jsonl")

tagged_count = 0

for filename in os.listdir(CLOSET_DIR):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        full_path = os.path.join(CLOSET_DIR, filename)
        result = tag_closet_item(full_path)

        if "error" in result:
            print(f"[!] Error tagging {filename}: {result['error']}")
            continue

        with open(OUTPUT_FILE, "a") as f:
            f.write(json.dumps(result) + "\n")

        tagged_count += 1
        print(f"[+] Tagged {filename} → {result}")

print(f"\n✅ Done! {tagged_count} items saved to inventory.jsonl")
