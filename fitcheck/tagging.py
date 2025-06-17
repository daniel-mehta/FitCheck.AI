import os
import json
import re
from PIL import Image
import imagehash
from streamlit import image
import torch
from transformers import Blip2Processor, Blip2ForConditionalGeneration


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load InstructBLIP model + processor
processor = Blip2Processor.from_pretrained("Salesforce/blip2-flan-t5-xl")
model = Blip2ForConditionalGeneration.from_pretrained(
    "Salesforce/blip2-flan-t5-xl", torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
).to(device)

'''
PROMPT = (
    "Look at the outfit in this image and extract the following attributes.\n"
    "Only answer using JSON format. Do not explain anything.\n\n"
    "Keys:\n"
    "- item_type: The main clothing item (e.g., 'shirt', 'jacket', 'pants', 'hoodie', 'dress', 'hat', 'suspenders')\n"
    "- color: The primary visible color of the main clothing item (e.g., 'black', 'blue', 'red')\n"
    "- indoor_outdoor: Is the person indoors or outdoors? Only answer with 'Indoor' or 'Outdoor'.\n\n"
    "Respond strictly like this:\n"
    "{ \"item_type\": \"<item>\", \"color\": \"<color>\", \"indoor_outdoor\": \"<Indoor/Outdoor>\" }"
)
'''
PROMPT = "What is the item_type, primary color, and indoor_or_outdoor setting of the outfit? "

def tag_closet_item(image_path: str) -> dict:
    """Generates a caption using BLIP, then extracts item_type, color, and indoor/outdoor from it."""
    try:
        image = Image.open(image_path).convert("RGB")

        # Stage 1: Generate caption
        caption_inputs = processor(image, PROMPT, return_tensors="pt")
        caption_inputs = {k: v.to(model.device) for k, v in caption_inputs.items()}

        caption_ids = model.generate(**caption_inputs, max_new_tokens=150)
        caption = processor.decode(caption_ids[0], skip_special_tokens=True)

        # Stage 2: Extract simple tags via heuristic
        # Example caption: "a man wearing a black hoodie and grey sweatpants standing outside"
        lower_caption = caption.lower()

        # Heuristic-based tag extraction
        item_type = "Unknown"
        color = "Unknown"
        indoor_outdoor = "Unknown"

        # Try to guess item_type from known words
        for keyword in ["shirt", "t-shirt", "hoodie", "jacket", "coat", "blazer", "sweater","pants", "jeans", "shorts", "trousers", "skirt", "dress","hat", "cap", "beanie", "suspenders","suspends", "glasses", "scarf", "boots", "shoes"]:
            if keyword in lower_caption:
                item_type = keyword.capitalize()
                break

        # Color
        for basic_color in ["black", "white", "grey", "gray", "blue", "red", "green", "yellow", "brown","beige", "orange", "purple", "pink", "navy", "gold", "silver"]:
            if basic_color in lower_caption:
                color = basic_color.capitalize()
                break

        # Indoor/outdoor
        if "outside" in lower_caption or "outdoor" in lower_caption:
            indoor_outdoor = "Outdoor"
        elif "inside" in lower_caption or "indoor" in lower_caption or "room" in lower_caption:
            indoor_outdoor = "Indoor"

        phash = str(imagehash.phash(image))

        print("[DEBUG] Caption:", caption)

        return {
            "image_id": phash,
            "item_type": item_type,
            "color": color,
            "indoor_outdoor": indoor_outdoor,
            "path": image_path,
            "folder": "Closet",
            "caption": caption  # Optional: keep for debugging
        }

    except Exception as e:
        return {"error": str(e)}
