from transformers import BertTokenizer, BertForSequenceClassification
import torch

# Load model once
tokenizer = BertTokenizer.from_pretrained("yiyanghkust/finbert-tone")
model = BertForSequenceClassification.from_pretrained("yiyanghkust/finbert-tone")

def get_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        logits = model(**inputs).logits
    probs = torch.softmax(logits, dim=1).numpy()[0]
    sentiment_score = round(probs[2] - probs[0], 3)
    return {
        "Negative": round(probs[0], 3),
        "Neutral": round(probs[1], 3),
        "Positive": round(probs[2], 3),
        "Score": sentiment_score
    }

def analyze_sentiment(text):
    return get_sentiment(text)