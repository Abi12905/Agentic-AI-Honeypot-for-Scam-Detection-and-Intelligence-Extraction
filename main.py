from fastapi import FastAPI, Header, HTTPException
import pickle
import re
import random

app = FastAPI()

# ====== API KEY ======
API_KEY = "my1secret2key3"

# ====== Load ML model ======
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

# ====== Agentic replies ======
AGENT_REPLIES = [
    "Oh no 😟 I am really scared. What should I do now?",
    "I don’t understand this. Can you explain slowly?",
    "Is my money safe? Please guide me.",
    "I have never faced this before. What is the next step?",
    "Can I pay later? I am confused."
]

@app.post("/honeypot")
def honeypot(data: dict, x_api_key: str = Header(None)):
    # 🔐 API key check
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    message = data.get("message", "")

    # ===== ML prediction =====
    msg_vector = vectorizer.transform([message])
    prediction = model.predict(msg_vector)[0]
    confidence = model.predict_proba(msg_vector)[0][prediction]

    is_scam = bool(prediction)

    # ===== Intelligence extraction =====
    upi_ids = re.findall(r'\b[\w.-]+@[\w.-]+\b', message)
    bank_accounts = re.findall(r'\b\d{9,18}\b', message)
    links = re.findall(r'https?://[^\s]+', message)

    scam_type = "Unknown"
    if upi_ids:
        scam_type = "UPI Fraud"
    elif links:
        scam_type = "Phishing"
    elif bank_accounts:
        scam_type = "Bank Transfer Scam"

    return {
        "is_scam": is_scam,
        "scam_type": scam_type,
        "confidence": round(float(confidence), 2),
        "extracted_intelligence": {
            "upi_ids": upi_ids,
            "bank_accounts": bank_accounts,
            "phishing_links": links
        },
        "agent_reply": random.choice(AGENT_REPLIES)
    }
