# 🧵 FitCheck.AI Hackathon Pipeline (Saturday → Thursday)

🏁 **Submission Track**: Build a Personal AI Agent  
🎯 **Framing**: FitCheck.AI is a personalized fashion assistant that remembers your wardrobe, tracks your fit history, and suggests smart, evolving outfits. It's not just a model — it's your AI stylist agent.

---

## 📅 **Saturday — Ideation + Setup**
- ✅ Finalize scope (agree on MVP vs stretch)
- ✅ Assign roles:
  - VLM + tagging module
  - Outfit suggestion engine (LLM + LangChain)
  - DB & backend logic
  - Frontend (Streamlit / Flask)
- ✅ Set up:
  - GitHub repo
  - Shared doc for prompts, evaluation ideas, and roadmap
  - Local dev environments with Ollama, LangChain, FAISS, etc.

---

## 📅 **Sunday — VLM + Inventory Upload**
- 🔲 Build manual upload UI (image + metadata input)
- 🔲 Implement auto-tagging via VLM (BLIP-2, CLIP, or Gemini Vision)
- 🔲 Normalize outputs into a consistent JSON schema:
  ```json
  {
    "item_id": "123",
    "name": "black hoodie",
    "category": "outerwear",
    "tags": ["black", "hoodie", "casual"],
    "image_path": "uploads/black_hoodie.jpg"
  }
  ```
- 🔲 Store in local DB (SQLite for now)

---

## 📅 **Monday — Outfit Builder + Memory**
- 🔲 Outfit suggestion logic using LangChain + local LLM
- 🔲 Restrict suggestions to owned items only
- 🔲 Allow pinning/saving outfits
- 🔲 Add item-aware constraints:
  - "Avoid repeating same pants more than 2x/week"
  - "Balance colors across pieces"
- 🔲 Simulate reusability tracking (per item frequency)

---

## 📅 **Tuesday — Fit Rating + Agent Memory**
- 🔲 Compare uploaded outfit to inventory using VLM
- 🔲 Score based on:
  - Reuse
  - Variety
  - Fit cohesion
- 🔲 Feedback examples:
  > “You’ve worn this hoodie 4x in 10 days. Try your navy cardigan next time.”

- 🔲 Add memory log of previous outfits and scores
- 🔲 Begin compiling “agent behavior” patterns (learning style, changing suggestions)

---

## 📅 **Wednesday — Polish + Optional Features**
- 🔲 Add bonus: Shopping Assistant (mock Shopify or static JSON)
- 🔲 Add fit history timeline (show improvements, “monthly drip score”)
- 🔲 UI polish: navigation, outfit previews, filter by category/season
- 🔲 Final demo testing & judge script prep

---

## 📅 **Thursday — Final Submission**
- 🔲 Final end-to-end test with demo inventory
- 🔲 Record demo video (2–3 mins, ideally with humor + agent voice)
- 🔲 Write final README:
  - Features
  - Tech stack
  - Personal AI agent framing
  - Team bios + roles
- 🔲 Submit to Devpost / MLH portal
- 🔲 Celebrate in style 🎉🕺

---

