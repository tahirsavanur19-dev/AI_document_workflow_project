import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib

fraud_texts = [
    "You have won a lottery prize",
    "Claim your free cash now",
    "Urgent bank account verification required",
    "Investment opportunity double your money",
    "Congratulations you are selected for reward",
    "Scratch and win big money",
    "Limited time offer claim prize now",
    "Transfer money immediately to secure account",
    "You are selected for lucky draw",
    "Free bonus waiting for you",
    "Verify your bank details urgently",
    "Click here to claim your reward",
    "Earn money quickly without work",
    "Get rich fast scheme",
    "Congratulations winner claim now",
    "Exclusive investment offer",
    "Double your income instantly",
    "Urgent action required on account",
    "Claim your cash prize today",
    "Lottery winner announcement"
]

safe_texts = [
    "Meeting scheduled tomorrow",
    "Project report submission",
    "Happy birthday wishes",
    "Lunch at 2 pm",
    "Team meeting agenda discussion",
    "Invoice attached for payment",
    "Client presentation update",
    "Please review the document",
    "Assignment submission deadline",
    "Conference call at 4 pm",
    "Budget planning discussion",
    "Office event invitation",
    "Weekly status update",
    "Training session reminder",
    "Holiday announcement",
    "Monthly performance review",
    "Internal audit report",
    "Company newsletter",
    "Staff meeting minutes",
    "Appointment confirmation"
]

texts = fraud_texts + safe_texts
labels = ["fraud"] * len(fraud_texts) + ["safe"] * len(safe_texts)

df = pd.DataFrame({
    "text": texts,
    "label": labels
})

model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", MultinomialNB())
])

model.fit(df["text"], df["label"])

joblib.dump(model, "fraud_model.pkl")

print("Improved model trained successfully!")