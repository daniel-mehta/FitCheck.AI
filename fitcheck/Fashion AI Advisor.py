import streamlit as st
from PIL import Image
import io
import imagehash
from analyze_outfit import analyze_outfit_tool, extract_comment, extract_rating, extract_style_paragraph
import dns 
from pymongo import MongoClient
from datetime import datetime, timezone
import os
import tenacity
import random

# Run with:
# streamlit run "fitcheck\Fashion AI Advisor.py"


# -------------------------------------------------------
# Workaround: prevent Streamlit from monitoring Torch's 
# internal modules (avoids runtime errors in some setups).
# -------------------------------------------------------
import sys
import types
sys.modules["torch.classes"] = types.ModuleType("torch.classes")
sys.path = [p for p in sys.path if "site-packages" not in p]

# -------------------------------------------------------
# MongoDB Client Setup
# -------------------------------------------------------
def get_mongo_client():
    """Initialize MongoDB connection.
    
    NOTE: URI is hardcoded here for demo purposes.
    In production, this should be stored in Streamlit 
    secrets or environment variables for security.
    """
    MONGO_URI = "mongodb+srv://dbMaster:dbMasterPassword@freeimagecluster.jjdz9nb.mongodb.net/?retryWrites=true&w=majority&appName=FreeImageCluster"

    return MongoClient(MONGO_URI)

# -------------------------------------------------------
# Streamlit Page Configuration
# -------------------------------------------------------
st.set_page_config(page_title="Fashion AI Advisor", layout="centered")

# Random emoji for fun, makes the UI feel fresh
clothing_emojis = ["👕", "👖", "👗", "🧥", "👔", "🩳", "🧢", "👚", "👘", "🥿", "👟", "🥾"]
title_emoji = random.choice(clothing_emojis)

st.title(f"{title_emoji} Outfit Analyzer")
st.markdown("Upload your outfit photo for instant analysis")

# -------------------------------------------------------
# File Upload Widget
# -------------------------------------------------------
uploaded_file = st.file_uploader(
    "Choose an outfit image", 
    type=["jpg", "jpeg", "png"],
    help="Full-body photos work best"
)


# -------------------------------------------------------
# Main Processing Logic
# -------------------------------------------------------
if uploaded_file is not None:
    # Process the image
    with st.spinner("Analyzing your outfit..."):
        try:
            # Open and display image
            image = Image.open(uploaded_file)
            st.image(image, caption="Your uploaded outfit", width=300)
            
            # Compute perceptual hash for duplicate detection
            phash = str(imagehash.phash(image))
            
            # Save temporarily for model analysis
            image_dir = os.path.join(os.path.dirname(__file__), "..", "Images")
            os.makedirs(image_dir, exist_ok=True)
            temp_path = os.path.join(image_dir, "temp_upload.jpg")
            image.save(temp_path)

            # Connect to MongoDB (Database: FashionAI, Collection: OutfitStorage)
            client = get_mongo_client()
            db = client.FashionAI # database name
            outfits = db.OutfitStorage   # collection name

            # Check if this outfit has already been analyzed (by hash)
            existing = outfits.find_one({"image_hash": phash})
            if existing:
                st.warning("This outfit was already analyzed before!")
                st.text(existing["analysis_result"])
                st.stop()  # Stop early if duplicate
            
            # Run AI analysis via LangChain tool wrapper
            analysis_result = analyze_outfit_tool.invoke(os.path.abspath(temp_path))

            # Clean up temporary file
            os.remove(temp_path)
            
            # Prepare MongoDB document with parsed results
            outfit_doc = {
                "image_hash": phash,
                "upload_date": datetime.now(timezone.utc),
                "rating": extract_rating(analysis_result),
                "style": extract_style_paragraph(analysis_result),
                "comment": extract_comment(analysis_result),
                "metadata": {
                    "filename": uploaded_file.name,
                    "size": uploaded_file.size,
                    "content_type": uploaded_file.type
                },
                "analysis_date": datetime.now(timezone.utc)
            }
            
            # Insert document into MongoDB
            result = outfits.insert_one(outfit_doc)
            
            # Display results to the user
            st.subheader("Analysis Results")
            st.markdown(analysis_result.encode('utf-8', errors='replace').decode('utf-8'), unsafe_allow_html=True)
            
            st.success(f"✅ Outfit analysis saved to database with ID: {result.inserted_id}")
            
        except Exception as e:
            # Catch errors gracefully and show in UI
            st.error(f"Error processing image: {str(e)}")
