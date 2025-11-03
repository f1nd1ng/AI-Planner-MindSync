# emotion_model.py
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

def load_emotion_model(model_name="bhadresh-savani/distilbert-base-uncased-emotion"):
    """
    Loads a pre-trained emotion detection model.
    Returns a tuple of (tokenizer, model, id2label mapping)
    """
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    id2label = model.config.id2label
    return tokenizer, model, id2label


def predict_emotion(text, tokenizer, model, id2label):
    """
    Predicts emotion and confidence score for a given text.
    Returns: (emotion_label, confidence)
    """
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    outputs = model(**inputs)
    probs = torch.nn.functional.softmax(outputs.logits, dim=1)
    pred_id = torch.argmax(probs).item()
    emotion = id2label[pred_id]
    confidence = probs[0][pred_id].item()
    return emotion, confidence
