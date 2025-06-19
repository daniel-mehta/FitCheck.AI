import streamlit as st
import os
import json
import random
import json
from typing import List, Dict, Optional
from pathlib import Path

# Classes used by streamlit for Closet

# recommendation system

# Color theory - compatible colors
COLOR_COMPATIBILITY = {
    "black": ["white", "gray", "red", "gold", "silver", "pink"],
    "white": ["black", "navy", "red", "green", "blue", "pink", "purple"],
    "grey": ["pink", "red", "white", "black", "navy"],
    "gray": ["pink", "red", "white", "black", "navy"],
    "blue": ["white", "grey", "beige", "brown", "orange"],
    "red": ["black", "white", "grey", "blue", "gold"],
    "green": ["white", "black", "brown", "beige", "gold"],
    "yellow": ["gray", "black", "blue", "purple"],
    "brown": ["beige", "blue", "green", "white"],
    "beige": ["brown", "blue", "green", "black"],
    "orange": ["blue", "white", "black"],
    "purple": ["yellow", "white", "gray", "black"],
    "pink": ["black", "white", "gray", "navy"],
    "navy": ["white", "pink", "gold", "gray"],
    "gold": ["black", "navy", "green", "red"],
    "silver": ["black", "white", "blue", "red"]
}

# Class that is basically a python object version of the JSON data
class ClothingItem:
    def __init__(self, data: Dict):
        self.name = data.get("name", "Unnamed")
        self.item_type = data.get("item_type", "unknown")
        self.color = data.get("color", "unknown")
        self.location = data.get("location", "Indoor")
        self.formality = data.get("formality", "Casual")
        self.gender = data.get("gender", "Unisex")
        self.image_path = data.get("image_path", "")
        
    def __repr__(self):
        return f"{self.name} ({self.color} {self.item_type})"

# Class that handles rule-based logic to recommend outfits
class OutfitRecommender:
    def __init__(self, data_folder: str):
        self.data_folder = data_folder
        self.clothing_items = self.load_clothing_items()
        
    def load_clothing_items(self) -> List[ClothingItem]:
        items = []
        for filename in os.listdir(self.data_folder):
            if filename.endswith(".json"):
                filepath = os.path.join(self.data_folder, filename)
                with open(filepath, "r") as f:
                    try:
                        data = json.load(f)
                        items.append(ClothingItem(data))
                    except json.JSONDecodeError:
                        st.warning(f"Could not decode {filename}")
        return items
    
    def filter_items(self, item_type: Optional[str] = None, 
                    color: Optional[str] = None,
                    location: Optional[str] = None,
                    formality: Optional[str] = None,
                    gender: Optional[str] = None) -> List[ClothingItem]:
        filtered = self.clothing_items
        
        if item_type:
            filtered = [item for item in filtered if item.item_type == item_type]
        if color:
            filtered = [item for item in filtered if item.color == color]
        if location:
            filtered = [item for item in filtered if item.location == location]
        if formality:
            filtered = [item for item in filtered if item.formality == formality]
        if gender:
            filtered = [item for item in filtered if item.gender == gender or item.gender == "Unisex"]
            
        return filtered
    
    def get_compatible_colors(self, color: str) -> List[str]:
        return COLOR_COMPATIBILITY.get(color.lower(), [])
    
    def recommend_outfit(self, location: str, formality: str, gender: str, base_color: Optional[str] = None) -> Dict[str, ClothingItem]:
        outfit = {}
        
        # Determine which item types we need for this outfit
        required_types = []
        if formality == "Formal":
            if gender == "Men's":
                required_types = ["shirts", "pants", "shoes", "jackets"]
            else:
                required_types = ["dresses", "shoes", "bags"]
        else:  # Casual
            if gender == "Men's":
                required_types = ["shirts", "pants", "shoes"]
            else:
                required_types = ["shirts", "pants", "shoes", "skirts"]
        
        # If outdoors, add accessories
        if location == "Outdoor":
            required_types.extend(["hats", "sunglasses"])
        
        # Find items for each required type
        for item_type in required_types:
            candidates = self.filter_items(
                item_type=item_type,
                location=location,
                formality=formality,
                gender=gender
            )
            
            # Filter by color compatibility if base color is provided
            if base_color and candidates:
                compatible_colors = self.get_compatible_colors(base_color)
                compatible_candidates = [item for item in candidates if item.color in compatible_colors]
                if compatible_candidates:
                    candidates = compatible_candidates
            
            if candidates:
                outfit[item_type] = random.choice(candidates)
                # Use the first item's color as base if not specified
                if base_color is None:
                    base_color = outfit[item_type].color
        
        return outfit

def display_outfit(outfit: Dict[str, ClothingItem]):
    st.subheader("Recommended Outfit")
    
    cols = st.columns(3)
    col_idx = 0
    
    for item_type, item in outfit.items():
        with cols[col_idx]:
            st.markdown(f"**{item_type.capitalize()}**")
            st.write(item.name)
            st.write(f"Color: {item.color}")
            st.write(f"Type: {item.formality}")
            
            # If you have images in your JSON data
            if item.image_path and os.path.exists(item.image_path):
                st.image(item.image_path, width=150)
        
        col_idx = (col_idx + 1) % 3

def main():
    st.set_page_config(page_title="Outfit Recommender", page_icon="👕")

    # Get the correct closet path (two levels up from this file)
    current_dir = Path(__file__).parent
    closet_path = current_dir.parent.parent / "Closet"
    
    # App title with random clothing emoji
    clothing_emojis = ["👕", "👖", "👗", "🧥", "👔", "🩳", "🧢", "👚", "👘", "🥿", "👟", "🥾"]
    st.title(f"{random.choice(clothing_emojis)} Outfit Recommender")
    
    # Initialize recommender
    if 'recommender' not in st.session_state:
        with st.spinner("Loading your closet..."):
            st.session_state.recommender = OutfitRecommender(str(closet_path)) # specify path to closet folder
    
    # User preferences form
    with st.form("preferences_form"):
        st.subheader("Outfit Preferences")
        
        col1, col2 = st.columns(2)
        with col1:
            location = st.selectbox("Location", ["Indoor", "Outdoor"])
            gender = st.selectbox("Gender", ["Men's", "Women's", "Unisex"])
        with col2:
            formality = st.selectbox("Formality", ["Formal", "Casual"])
            color_preference = st.selectbox("Preferred Color (optional)", [""] + sorted(list(COLOR_COMPATIBILITY.keys())))
        
        submitted = st.form_submit_button("Recommend Outfit")
    
    # Generate and display outfit when form is submitted
    if submitted:
        if not os.path.exists(str(closet_path)):
            st.error("Closet directory not found. Please create a 'Closet' folder with your clothing items.")
            return
        
        if not st.session_state.recommender.clothing_items:
            st.warning("Your closet is empty! Add some clothing items first.")
            return
        
        outfit = st.session_state.recommender.recommend_outfit(
            location=location,
            formality=formality,
            gender=gender,
            base_color=color_preference if color_preference else None
        )
        
        if outfit:
            display_outfit(outfit)
        else:
            st.warning("No matching outfit found. Try different criteria or add more clothing items.")

main()