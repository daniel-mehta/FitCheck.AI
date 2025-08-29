import os
import json
from PIL import Image
import imagehash
import torch
from transformers import CLIPProcessor, CLIPModel

# -------------------------------------------------------
# Device setup (use GPU if available, otherwise CPU)
# -------------------------------------------------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# -------------------------------------------------------
# Load CLIP model & processor
# -------------------------------------------------------
# CLIP can compare text labels with image embeddings.
# Here we use the pretrained "ViT-B/32" variant.
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)

# -------------------------------------------------------
# Label sets for classification
# -------------------------------------------------------
# Each list contains candidate labels for one category.
# CLIP encodes both the image and each text label into the
# same embedding space. It then compares them using cosine 
# similarity (returned as logits_per_image). 
# The label with the highest similarity score is selected.
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


# -------------------------------------------------------
# Helper function: classify
# -------------------------------------------------------
def classify(image, labels):
    """
    Given an image and a list of labels, return the label 
    with the highest similarity according to CLIP.
    """
    # Encode both the text labels and the image
    inputs = processor(text=labels, images=image, return_tensors="pt", padding=True).to(device)
    outputs = model(**inputs)

    # Compare embeddings: logits_per_image gives similarity
    logits = outputs.logits_per_image
    probs = logits.softmax(dim=1)
    
    # Pick the label with highest probability
    best_idx = probs.argmax().item()
    return labels[best_idx]

# -------------------------------------------------------
# Main function: tag_closet_item
# -------------------------------------------------------
def tag_closet_item(image_path: str) -> dict:
    """
    Tag a clothing item image with:
    - item type (shirt, shoes, etc.)
    - color
    - indoor/outdoor
    - formality (formal/casual)
    - gender style (men’s/women’s/unisex)

    Returns a structured JSON-like dictionary.
    """
    try:
        # Load image in RGB mode
        image = Image.open(image_path).convert("RGB")
        
        # Perceptual hash for deduplication / ID
        phash = str(imagehash.phash(image))

        # Run CLIP classification for each attribute
        item_type = classify(image, ITEM_LABELS).capitalize()
        color = classify(image, COLOR_LABELS).capitalize()

        # Special case: shoes are always "Outdoor"
        if item_type.lower() == "shoes":
            indoor_outdoor = "Outdoor"
        else:
            indoor_outdoor = classify(image, LOCATION_LABELS)

        formality = classify(image, FORMALITY_LABELS)
        gender = classify(image, GENDER_LABELS)

        # Return a normalized record
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
        # Gracefully handle errors (eg. unreadable image)
        return {"error": str(e)}

