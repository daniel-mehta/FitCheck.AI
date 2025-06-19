import os
import json
from PIL import Image
import imagehash
import torch
from transformers import CLIPProcessor, CLIPModel

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load CLIP processor + model
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)

# Label sets
ITEM_LABELS = [
    "sunglasses", "hats", "jackets", "shirts", "pants", "shorts",
    "skirts", "dresses", "bags", "shoes"
]


COLOR_LABELS = [
    "black", "white", "grey", "gray", "blue", "red", "green", "yellow", "brown", "beige",
    "orange", "purple", "pink", "navy", "gold", "silver"
]

LOCATION_LABELS = ["Indoor", "Outdoor"]
FORMALITY_LABELS = ["Formal", "Casual"]
GENDER_LABELS = ["Men's", "Women's", "Unisex"]

def classify(image, labels):
    """Return the label with highest similarity to the image."""
    inputs = processor(text=labels, images=image, return_tensors="pt", padding=True).to(device)
    outputs = model(**inputs)
    logits = outputs.logits_per_image
    probs = logits.softmax(dim=1)
    best_idx = probs.argmax().item()
    return labels[best_idx]

def tag_closet_item(image_path: str) -> dict:
    """Tag an outfit image with item type, color, setting, gender, and formality using CLIP."""
    try:
        image = Image.open(image_path).convert("RGB")
        phash = str(imagehash.phash(image))

        item_type = classify(image, ITEM_LABELS).capitalize()
        color = classify(image, COLOR_LABELS).capitalize()

        # Fix: define indoor_outdoor
        if item_type.lower() == "shoes":
            indoor_outdoor = "Outdoor"
        else:
            indoor_outdoor = classify(image, LOCATION_LABELS)

        formality = classify(image, FORMALITY_LABELS)
        gender = classify(image, GENDER_LABELS)

        return {
            "image_id": phash,
            "item_type": item_type,
            "color": color,
            "indoor_outdoor": indoor_outdoor,
            "formality": formality,
            "gender": gender,
            "path": image_path,
            "folder": "Closet"
        }

    except Exception as e:
        return {"error": str(e)}

