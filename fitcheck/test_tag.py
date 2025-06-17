import os
import json
from tagging import tag_closet_item

# Absolute path to test image
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TEST_IMAGE = os.path.join(BASE_DIR, "Images", "fit_look_02.jpg")

# Run tagging
result = tag_closet_item(TEST_IMAGE)

# Display result
print("\n🔍 Tagging Result:")
print(json.dumps(result, indent=2))

# Save JSON to Closet folder if successful
if "error" not in result:
    # Make sure Closet directory exists
    CLOSET_DIR = os.path.join(BASE_DIR, "Closet")
    os.makedirs(CLOSET_DIR, exist_ok=True)

    # Build JSON file path with same name as image
    base_name = os.path.splitext(os.path.basename(TEST_IMAGE))[0]
    out_path = os.path.join(CLOSET_DIR, f"{base_name}.json")

    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)

    print(f"\n✅ Saved to {out_path}")
else:
    print("\n❌ Tagging failed")
