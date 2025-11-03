# backend/core.py
import datetime, re
from typing import List, Dict, Tuple

# optional ML load (safe fallback if libs are missing)
try:
    import torch
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    _HAS_ML = True
except Exception:
    torch = None
    AutoTokenizer = AutoModelForSequenceClassification = None
    _HAS_ML = False

_EMOJI_MAP = {
    "joy": ("😄", "Joy"),
    "sadness": ("😢", "Sadness"),
    "anger": ("😡", "Anger"),
    "fear": ("😨", "Fear"),
    "optimism": ("😊", "Optimism"),
    "love": ("😍", "Love"),
    "neutral": ("🙂", "Neutral"),
}

_tokenizer = None
_model = None
_id2label = None

def _maybe_load_model():
    global _tokenizer, _model, _id2label
    if not _HAS_ML or _tokenizer is not None:
        return
    model_name = "j-hartmann/emotion-english-distilroberta-base"
    _tokenizer = AutoTokenizer.from_pretrained(model_name)
    _model = AutoModelForSequenceClassification.from_pretrained(model_name)
    _id2label = {int(k): v for k, v in _model.config.id2label.items()}

def _heuristic_emotion(text: str) -> Tuple[str, str, str, float]:
    t = text.lower()
    if any(x in t for x in ["happy", "excited", "optimistic", "great"]):
        return ("joy",) + _EMOJI_MAP["joy"] + (0.85,)
    if any(x in t for x in ["sad", "down", "tired", "exhausted", "anxious"]):
        return ("sadness",) + _EMOJI_MAP["sadness"] + (0.8,)
    if any(x in t for x in ["angry", "mad", "furious"]):
        return ("anger",) + _EMOJI_MAP["anger"] + (0.8,)
    if any(x in t for x in ["scared", "afraid", "worried", "panic"]):
        return ("fear",) + _EMOJI_MAP["fear"] + (0.75,)
    return ("neutral",) + _EMOJI_MAP["neutral"] + (0.6,)

def detect_emotion(text: str):
    """Return (label, friendly, emoji, confidence). Never raises for missing ML."""
    text = (text or "").strip()
    if not text:
        return ("neutral",) + _EMOJI_MAP["neutral"] + (0.0,)

    if not _HAS_ML:
        return _heuristic_emotion(text)

    try:
        _maybe_load_model()
        inputs = _tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = _model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=1)[0]
        idx = int(torch.argmax(probs))
        label = _id2label[idx].lower()
        emoji, friendly = _EMOJI_MAP.get(label, _EMOJI_MAP["neutral"])
        conf = float(probs[idx])
        return (label, friendly, emoji, conf)
    except Exception:
        # If ML path fails, fallback – keeps API stable
        return _heuristic_emotion(text)

def df_to_tasks(df) -> List[Dict]:
    tasks = []
    for _, r in df.iterrows():
        name = str(r.get("Task Name", "") or "").strip() or "Untitled Task"
        try:
            hours = int(r.get("Hours", 0) or 0)
        except Exception:
            hours = 0
        try:
            minutes = int(r.get("Minutes", 0) or 0)
        except Exception:
            minutes = 0
        tasks.append({"Task": name, "Duration (mins)": hours * 60 + minutes})
    return tasks

def make_events(tasks: List[Dict], start_dt: datetime.datetime, gap: int) -> List[Dict]:
    events = []
    now = start_dt
    for t in tasks:
        title = t.get("Task") or t.get("Task Name") or "Untitled Task"
        mins = int(t.get("Duration (mins)", 30))
        end = now + datetime.timedelta(minutes=mins)
        events.append({
            "title": title.strip() or "Untitled Task",
            "start": now.strftime("%Y-%m-%dT%H:%M:%S"),
            "end": end.strftime("%Y-%m-%dT%H:%M:%S"),
        })
        now = end + datetime.timedelta(minutes=gap)
    return events
