import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load dataset
df = pd.read_csv("scam_dataset.csv")

X = df["text"]
y = df["label"]

# Convert text to numbers
vectorizer = TfidfVectorizer(stop_words="english")
X_vectorized = vectorizer.fit_transform(X)

# Train ML model
model = LogisticRegression()
model.fit(X_vectorized, y)

# Save model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("✅ Model trained and saved successfully")
