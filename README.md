# 👔 FitCheck.AI

**Your closet-aware fashion critic.**  
FitCheckAI is a personal AI stylist that tags your clothes, roasts your fits, and builds outfits - all through an interactive Streamlit UI.

🎥 **Demo Video:** [https://youtu.be/s57yTOkLLwY](https://youtu.be/s57yTOkLLwY)

---

## 🚀 Features

### 🧠 1. Outfit Analyzer (LangChain + Qwen)
Upload a photo of your outfit and get a brutally honest AI critique, including:
- Style breakdown
- Score out of 100
- Savage one-liner

All results are saved to MongoDB and de-duplicated using perceptual hashing.

### 🧺 2. Smart Closet Tagging (CLIP)
Upload individual clothing items - the AI classifies:
- Item type (`shirt`, `shoes`, etc.)
- Color (`black`, `white`, etc.)
- Setting (`indoor/outdoor`)
- Formality
- Gender style

Saved in a consistent JSON format and stored in `/Closet`.

### 🧩 3. Outfit Generator
Generates full outfit recommendations based on:
- Location (indoor/outdoor)
- Formality (casual/formal)
- Gender
- Preferred color

Color compatibility rules are applied (e.g. blue pairs with beige, white, brown, etc).

---

## 🛠️ Tech Stack

| Component       | Tool / Library                         |
|------------------|----------------------------------------|
| UI               | Streamlit                              |
| Fashion Critique | LangChain + Qwen2.5 VL (3B, quantized) |
| Image Tagging    | CLIP (`openai/clip-vit-base-patch32`)  |
| Database         | MongoDB Atlas                          |
| Data Format      | JSON / `.jsonl`                        |

---

## 🗂️ Project Structure

```
.
├── fitcheck/
│   ├── Fashion AI Advisor.py         # Main Streamlit app
│   ├── analyze_outfit.py             # Outfit critic logic
│   ├── tagging.py                    # Tagging with CLIP
│   ├── tag_closet_items.py           # Bulk closet tagger
│   ├── test_Analyze_Outfit.py        # Unit test for LangChain outfit critique
│   ├── test_tag.py                   # Unit test for tagging module
│   ├── testmongoconnection.py        # MongoDB connection test
│   └── pages/
│       ├── 1_Add_to_Inventory.py     # Upload and tag closet items
│       └── 2_Get_Outfit_Suggestion.py# Outfit recommender (rule-based)
├── Closet/                           # JSON-tagged clothing items
├── Images/                           # Outfit photos
├── designs/                          # Wireframes + mockups
├── requirements.txt
├── run_app.bat
└── vlm_tagging_test.ipynb            # Prototype testing
```

---

## 🧪 Example Output

### **Critique Output**

![Outfit Critique](https://miro.medium.com/v2/resize:fit:810/0*nXX6k09Q9bobDelr.jpg)


**Style:** The outfit features a casual yet trendy ensemble consisting of a black beanie hat, a white scarf wrapped around the neck, a striped long-sleeve shirt under a black vest over jeans. The combination suggests an urban, laid-back vibe but lacks depth due to its simplicity.

**Rating:** 35/100

**Comment:** "This outfit might as well have been designed by a robot; it's so formulaic."


### **Closet JSON Schema**
```json
{
  "image_id": "abc123",
  "item_type": "Jacket",
  "color": "Black",
  "indoor_outdoor": "Outdoor",
  "formality": "Casual",
  "gender": "Men's",
  "path": "Closet/jacket.jpg",
  "folder": "Closet"
}
```


### **Outfit Recommender**
![Outfit Recommender](https://media.discordapp.net/attachments/1373125490034085984/1385256072763281418/image.png?ex=685567c0&is=68541640&hm=ca284b58e8b7f9c212f2c691194d3450ddd4c56a81677956c02b0738a629089b&=&format=webp&quality=lossless)

---
## 🖼️ UI Concept Designs

These were mockups used to guide layout and flow.

<p align="center">
  <img src="designs/Home Frame.png" width="600"/>
  <br/><em>Landing Page</em>
</p>

<p align="center">
  <img src="designs/Dropbox Frame.png" width="600"/>
  <br/><em>Upload Interface</em>
</p>

<p align="center">
  <img src="designs/Results Frame.png" width="600"/>
  <br/><em>LeCritique Display</em>
</p>

---

## ⚙️ Usage

Install dependencies:
```
pip install -r requirements.txt
```

Then launch the app:
```
streamlit run "fitcheck/Fashion AI Advisor.py"
```

---

## 👥 Team

- **Daniel Mehta**  
- **George Fotabong**
- **Dylan Higuchi**

---

## 🧩 Notes
- MongoDB URI is hardcoded for now (demo only - no sensitive data).

