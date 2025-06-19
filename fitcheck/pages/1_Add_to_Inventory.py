import streamlit as st
import os
import json
import random
from tagging import tag_closet_item

# Random clothing emoji for title
clothing_emojis = ["👕", "👖", "👗", "🧥", "👔", "🩳", "🧢", "👚", "👘", "🥿", "👟", "🥾"]
title_emoji = random.choice(clothing_emojis)

st.title(f"{title_emoji} Add Clothing to Inventory")

uploaded_file = st.file_uploader("Upload Photo of Clothing", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Save uploaded image to a temporary file
    temp_path = os.path.join("temp", uploaded_file.name)
    os.makedirs("temp", exist_ok=True)
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.read())

    st.image(temp_path, caption="Uploaded Clothing Image", use_container_width=True)

    # Tag the image
    with st.spinner("Analyzing clothing..."):
        result = tag_closet_item(temp_path)

    if "error" in result:
        st.error(f"Tagging failed: {result['error']}")
    else:
        st.success("Clothing tagged successfully!")
        st.subheader("🧷 Clothing Details")
        st.json(result)

        # Save JSON to Closet folder
        closet_dir = os.path.join("Closet")
        os.makedirs(closet_dir, exist_ok=True)

        base_name = os.path.splitext(uploaded_file.name)[0]
        out_path = os.path.join(closet_dir, f"{base_name}.json")
        with open(out_path, "w") as f:
            json.dump(result, f, indent=2)

        st.info(f"Metadata saved to `{out_path}`")
