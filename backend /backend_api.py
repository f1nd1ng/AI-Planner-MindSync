# backend_api.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import datetime as dt

# ---------- Optional ML (safe fallback if not installed) ----------
try:
    import torch
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    _HAS_ML = True
except Exception:
    torch = None
    AutoTokenizer = AutoModelForSequenceClassification = None
    _HAS_ML = False

_tokenizer = None
_model = None
_id2label = None

_EMOJI_MAP = {
    "joy": ("😄", "Joy"),
    "sadness": ("😢", "Sadness"),
    "anger": ("😡", "Anger"),
    "fear": ("😨", "Fear"),
    "optimism": ("😊", "Optimism"),
    "love": ("😍", "Love"),
    "neutral": ("🙂", "Neutral"),
}

def _maybe_load_model():
    global _tokenizer, _model, _id2label
    if not _HAS_ML or _tokenizer is not None:
        return
    model_name = "j-hartmann/emotion-english-distilroberta-base"
    _tokenizer = AutoTokenizer.from_pretrained(model_name)
    _model = AutoModelForSequenceClassification.from_pretrained(model_name)
    _id2label = {int(k): v for k, v in _model.config.id2label.items()}

def _heuristic_emotion(text: str):
    t = (text or "").lower()
    if any(w in t for w in ["happy", "great", "excited", "optimistic"]):
        return ("joy",) + _EMOJI_MAP["joy"] + (0.85,)
    if any(w in t for w in ["sad", "down", "tired", "exhausted", "anxious"]):
        return ("sadness",) + _EMOJI_MAP["sadness"] + (0.8,)
    if any(w in t for w in ["angry", "mad", "furious"]):
        return ("anger",) + _EMOJI_MAP["anger"] + (0.8,)
    if any(w in t for w in ["scared", "afraid", "worried", "panic"]):
        return ("fear",) + _EMOJI_MAP["fear"] + (0.75,)
    return ("neutral",) + _EMOJI_MAP["neutral"] + (0.6,)

def detect_emotion(text: str):
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
        return _heuristic_emotion(text)

def emotion_to_strategy(label: Optional[str]) -> str:
    if not label:
        return "neutral"
    label = label.lower()
    low = {"sadness", "fear", "anger"}
    high = {"joy", "optimism", "love"}
    if label in low: return "short-first"
    if label in high: return "long-first"
    return "neutral"

def make_events(tasks, start_dt: dt.datetime, gap: int):
    events = []
    now = start_dt
    for t in tasks:
        title = t.get("Task") or t.get("Task Name") or "Untitled Task"
        mins = int(t.get("Duration (mins)", 30))
        end = now + dt.timedelta(minutes=mins)
        events.append({
            "title": (title or "Untitled Task").strip(),
            "start": now.strftime("%Y-%m-%dT%H:%M:%S"),
            "end": end.strftime("%Y-%m-%dT%H:%M:%S")
        })
        now = end + dt.timedelta(minutes=gap)
    return events

# ---------- FastAPI ----------
app = FastAPI(title="MindSync API", version="1.0")

# CORS (allow Vite dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MoodIn(BaseModel):
    text: str

class TaskIn(BaseModel):
    name: str
    hours: int = 0
    minutes: int = 0

class ScheduleIn(BaseModel):
    tasks: List[TaskIn]
    mood_label: Optional[str] = "neutral"
    start_time: str = "09:00"
    break_min: int = 10

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/detect_mood")
def detect_mood_api(body: MoodIn):
    try:
        label, friendly, emoji, conf = detect_emotion(body.text or "")
        label = label or "neutral"
        return {"label": label, "friendly": friendly, "emoji": emoji, "confidence": conf}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"detect_mood failed: {type(e).__name__}: {e}")

@app.post("/generate_schedule")
def generate_schedule_api(body: ScheduleIn):
    try:
        label = (body.mood_label or "neutral").lower()
        strategy = emotion_to_strategy(label)

        # reorder by strategy
        tasks = list(body.tasks)
        if strategy == "long-first":
            tasks.sort(key=lambda t: -((t.hours or 0) * 60 + (t.minutes or 0)))
        elif strategy == "short-first":
            tasks.sort(key=lambda t: ((t.hours or 0) * 60 + (t.minutes or 0)))

        rows = [{"Task": (t.name or "").strip() or "Untitled Task",
                 "Duration (mins)": (t.hours or 0) * 60 + (t.minutes or 0)} for t in tasks]

        h, m = [int(x) for x in body.start_time.split(":")]
        start_dt = dt.datetime.combine(dt.date.today(), dt.time(h, m))
        evs = make_events(rows, start_dt, body.break_min)

        return {"events": evs, "strategy": strategy}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"generate_schedule failed: {type(e).__name__}: {e}")

@app.get("/")
def root():
    return {"ok": True, "message": "MindSync API running. See /docs"}
