import streamlit as st
from PIL import Image
import io
import imagehash
from analyze_outfit import analyze_outfit_tool, extract_comment, extract_rating, extract_style_paragraph
from pymongo import MongoClient
from datetime import datetime
import os

# MongoDB Setup
def get_mongo_client():
    """Initialize MongoDB connection"""
    # Replace with your actual connection string
    # MONGO_URI = st.secrets["mongodb"]["uri"]  # Store in Streamlit secrets
    MONGO_URI = "mongodb+srv://dbMaster:dbMasterPassword@freeimagecluster.jjdz9nb.mongodb.net/?retryWrites=true&w=majority&appName=FreeImageCluster"

    return MongoClient(MONGO_URI)

# Configure page
st.set_page_config(page_title="Fashion AI Advisor", layout="centered")

# App title and description
st.title("👕 Outfit Analyzer")
st.markdown("Upload your outfit photo for instant analysis")

# File uploader
uploaded_file = st.file_uploader(
    "Choose an outfit image", 
    type=["jpg", "jpeg", "png"],
    help="Full-body photos work best"
)

if uploaded_file is not None:
    # Process the image
    with st.spinner("Analyzing your outfit..."):
        try:
            # Open and display image
            image = Image.open(uploaded_file)
            st.image(image, caption="Your uploaded outfit", width=300)
            
            # Generate image hash
            phash = str(imagehash.phash(image))
            
            # Save to temporary file for analysis
            temp_path = "..\Images\temp_upload.jpg"
            image.save(temp_path)

            # Connect to MongoDB
            client = get_mongo_client()
            db = client.FashionAI # database name
            outfits = db.OutfitStorage   # collection name

            # Check if this image already exists in DB
            existing = outfits.find_one({"image_hash": phash})
            if existing:
                st.warning("This outfit was already analyzed before!")
                st.text(existing["analysis_result"])
                st.stop()  # Halt further processing
            
            # Call your analysis function
            analysis_result = analyze_outfit_tool.invoke(temp_path)
            
            # Clean up temp file
            os.remove(temp_path)
            
            # Prepare document for MongoDB
            outfit_doc = {
                "image_hash": phash,
                "upload_date": datetime.now(datetime.timezone.utc),
                "rating": extract_rating(analysis_result),
                "style": extract_style_paragraph(analysis_result),
                "comment": extract_comment(analysis_result),
                "metadata": {
                    "filename": uploaded_file.name,
                    "size": uploaded_file.size,
                    "content_type": uploaded_file.type
                },
                "analysis_date": datetime.now(datetime.timezone.utc)
            }
            
            # Insert into MongoDB
            result = outfits.insert_one(outfit_doc)
            
            # Display results
            st.subheader("Analysis Results")
            st.text(analysis_result.encode('utf-8', errors='replace').decode('utf-8'))
            
            st.success(f"✅ Outfit analysis saved to database with ID: {result.inserted_id}")
            
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")