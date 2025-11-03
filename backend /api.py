# api.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import datetime
import pandas as pd

# reuse your working logic from app.py
from app import detect_emotion, df_to_tasks, make_events

app = FastAPI(title="MindSync API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class MoodRequest(BaseModel):
    text: str

@app.post("/detect_mood")
def detect_mood_api(body: MoodRequest):
    label, friendly, emoji, conf = detect_emotion(body.text)
    return {"label": label, "friendly": friendly, "emoji": emoji, "confidence": conf}

class TaskItem(BaseModel):
    name: str
    hours: int
    minutes: int

class ScheduleRequest(BaseModel):
    tasks: list[TaskItem]
    start_time: str
    break_min: int

@app.post("/generate_schedule")
def generate_schedule_api(body: ScheduleRequest):
    df = pd.DataFrame(
        [{"Task Name": t.name, "Hours": t.hours, "Minutes": t.minutes} for t in body.tasks]
    )
    tasks = df_to_tasks(df)
    h, m = map(int, body.start_time.split(":"))
    start_dt = datetime.datetime.combine(datetime.date.today(), datetime.time(h, m))
    events = make_events(tasks, start_dt, body.break_min)
    return {"events": events}

@app.get("/")
def root():
    return {"ok": True, "message": "MindSync API running. See /docs"}
