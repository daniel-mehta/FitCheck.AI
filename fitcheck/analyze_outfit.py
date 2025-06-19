"""
Provides a function to analyze fashion images using Qwen2.5-VL.
Loads images from the 'Images' folder, applies a fashion critique prompt,
and returns structured style, rating, and commentary output.
"""

from PIL import Image
import torch
from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
from langchain.tools import tool
import os
import re
from modelscope import AutoProcessor, Qwen2_5_VLForConditionalGeneration


# Load model & processor (on module load)
# Use quantized 3B model
model_id = "Qwen/Qwen2.5-VL-3B-Instruct-AWQ"

processor = AutoProcessor.from_pretrained(model_id)
model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
    model_id,
    torch_dtype=torch.float16,
    device_map="auto"
)

# Folder where images are stored
IMAGE_DIR = "Images"

# Fashion prompt template
FASHION_PROMPT = (
    "You're a ruthless, stylish fashion critic with zero tolerance for mediocrity. "
    "Your job is to judge this outfit with sharp precision and brutal honesty. "
    "Forget politeness — if it’s boring, mismatched, or unoriginal, tear it apart. "
    "Only truly exceptional style earns praise, and even then, make them fight for it.\n\n"
    "Follow this exact format, don't deviate from it:\n"
    "Style: [Clear, blunt breakdown of the clothing and overall aesthetic — call out strengths and weaknesses with no filter]\n"
    "Rating: [Score out of 100 — average is 45. Weak or ugly fits land in the 20–45 range. Only elite looks should break 80]\n"
    "Comment: [Savage one-liner — roast it if it deserves it, or give reluctant praise if it's genuinely stylish. No fluff, no mercy.]"
)

# Image loader
def get_image(image_name: str) -> Image.Image:
    image_path = os.path.join(IMAGE_DIR, image_name)
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")
    return Image.open(image_path).convert("RGB")

# Extract rating score from AI output
def extract_rating(text):
    # using this means that we need to state in the prompt that "Rating: xx/100" must appear in the output exactly once"
    match = re.search(r'Rating:\s*(\d+)/100', text)
    if match:
        score = int(match.group(1))
        return score / 100.0
    return None  # or raise an error / default value

# Extract style comments from AI output
def extract_style_paragraph(text):
    match = re.search(r'Style:\s*(.*?)(?=\s*(Rating:|Comment:|$))', text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

# Extract comments for improvement from AI output
def extract_comment(text):
    match = re.search(r'Comment:\s*(.*)', text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

# Outfit analyzer tool
def analyze_outfit(image_name: str) -> str:
    """
    Analyze the outfit in the given image (from the Images/ folder) and return a structured critique.
    """
    print(f"[DEBUG] Loading image: {image_name}")
    print("[DEBUG] CWD:", os.getcwd())
    print("[DEBUG] Expected path:", os.path.join(IMAGE_DIR, image_name))

    img = get_image(image_name)

    print("[DEBUG] Creating message payload")
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": img},
                {"type": "text", "text": FASHION_PROMPT},
            ],
        }
    ]

    print("[DEBUG] Applying chat template")
    text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

    print("[DEBUG] Preprocessing input")
    inputs = processor(text=[text], images=[img], padding=True, return_tensors="pt").to("cuda")

    print("[DEBUG] Running model.generate()")
    outputs = model.generate(
        **inputs,
        max_new_tokens=256,
        temperature=0.8,
        top_p=0.95,
        repetition_penalty=1.2,
        do_sample=True,
        eos_token_id=processor.tokenizer.eos_token_id
    )

    print("[DEBUG] Trimming generated tokens")
    generated_ids_trimmed = [out[len(inp):] for inp, out in zip(inputs.input_ids, outputs)]

    print("[DEBUG] Decoding response")
    result = processor.batch_decode(generated_ids_trimmed, skip_special_tokens=True)

    print("[DEBUG] Output ready")
    return result[0]

@tool
def analyze_outfit_tool(image_name: str) -> str:
    """
    LangChain tool version of the outfit analyzer.
    Input: image filename located in 'Images/' folder.
    Output: Model's style, rating, and comment critique.
    """
    return analyze_outfit(image_name)