# TODO

- Refine the prompt for edge cases that's not an outfit or a complete outfit
  - Use LangChain
    - Tell the user why the image is not good for this
- Gives ideas or suggestions
- Take stored outfits and mix and match
- Picture of clothing in the database
- Add seeding to the model
  - Hyperparameter training

---

## Order 
1. A Langchain function that runs basic version in py file (With Prompt engineering)
2. Get Images Tokenized
3. Put Images in the DB
4. Langchain Pipeline
5. Integrate Langchain with VLM and Database
6. Frontend


---

## Database Type
### MongoDB Atlas
**Why: Fully managed, easy to set up, has a free tier, and great for storing images (using GridFS for larger files)**

- Store image with classification
  - Type: Shirt, Pants, Accessory (anything that doesn't fit other categories), shoe, outerwear
  - Short Description of each 

Setup:
```
Create an account at mongodb.com/atlas

Create a free cluster

Add your peers as database users

Whitelist IP addresses (or allow all for development)

Use connection strings to share access
```

---

## Langchain
- Determine if clothing should be added to the database
- Rejects user input

Download:
```bash
pip install langchain-core langchain-community
```

---

## Docker
- Implement Docker

---

## Model

Model: [Qwen2.5-VL-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-VL-7B-Instruct)

---

## UI

Streamlit

```bash
pip install streamlit
```
