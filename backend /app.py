# app.py
import streamlit as st
import datetime
import pandas as pd
import json
import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from streamlit_calendar import calendar
from ics import Calendar, Event
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import pickle

# ------------------ Page Config ------------------
st.set_page_config(page_title="🧠 MindSync", layout="wide")
st.title("🧠 MindSync — Emotion-Aware Smart Scheduler")

# ------------------ Emotion Model ------------------
@st.cache_resource(show_spinner=False)
def load_emotion_model():
    try:
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        import torch as _torch

        model_name = "j-hartmann/emotion-english-distilroberta-base"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        id2label = {int(k): v for k, v in model.config.id2label.items()}
        return tokenizer, model, id2label, None
    except Exception as e:
        # Return None to let the app continue and show a friendly message
        return None, None, None, e

tokenizer, model, id2label, _load_err = load_emotion_model()
if _load_err:
    st.warning(
        "⚠️ The emotion model couldn’t be loaded. "
        "Please update your Python packages: `pip install -U \"torch>=2.2\" \"transformers>=4.42\"`.\n\n"
        f"Details: `{type(_load_err).__name__}: {_load_err}`"
    )

def detect_emotion(text):
    if not text.strip() or tokenizer is None or model is None:
        # graceful fallback
        return None, "Neutral", "😐", 0.0
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    scores = torch.nn.functional.softmax(outputs.logits, dim=1)[0]
    best_idx = torch.argmax(scores).item()
    label = id2label[best_idx].lower()
    emoji, friendly = EMOJI_MAP.get(label, ("🙂", label.capitalize()))
    confidence = float(scores[best_idx])
    return label, friendly, emoji, confidence

# ------------------ Session Setup ------------------
if "tasks_df" not in st.session_state:
    st.session_state.tasks_df = pd.DataFrame(columns=["Task Name", "Hours", "Minutes"])
if "detected_mood" not in st.session_state:
    st.session_state.detected_mood = None
if "events" not in st.session_state:
    st.session_state.events = []

# ------------------ Step 1: Mood ------------------
st.markdown("---")
st.header("🌤️ Step 1 — Describe your mood")
mood_input = st.text_area("How are you feeling today?")

col_m1, col_m2 = st.columns([1, 2])
with col_m1:
    if st.button("🧠 Detect Mood"):
        label, friendly, emoji, conf = detect_emotion(mood_input)
        st.session_state.detected_mood = {
            "label": label, "friendly": friendly, "emoji": emoji, "confidence": conf
        }

with col_m2:
    dm = st.session_state.detected_mood
    if dm:
        conf_pct = int(dm["confidence"] * 100)
        st.success(f"Detected mood: **{dm['friendly']}** {dm['emoji']} ({conf_pct}%)")
    else:
        st.info("Click Detect Mood to analyze your input.")

# ------------------ Step 2: Tasks ------------------
st.markdown("---")
st.header("🗒️ Step 2 — Add your tasks")

edited_df = st.data_editor(
    st.session_state.tasks_df,
    num_rows="dynamic",
    use_container_width=True,
    key="task_editor"
)

if st.button("💾 Save Tasks"):
    st.session_state.tasks_df = edited_df.copy()
    st.success("✅ Tasks saved successfully!")

# ------------------ Step 3: Day Settings ------------------
st.markdown("---")
st.header("⚙️ Step 3 — Customize your day")

col1, col2, col3 = st.columns(3)
with col1:
    start_time = st.time_input("Start time", datetime.time(9, 0))
with col2:
    break_min = st.number_input("Break between tasks (mins)", 0, 180, 10)
with col3:
    timezone = st.selectbox("Timezone", ["Asia/Kolkata", "UTC", "US/Eastern", "Europe/London"], 0)

# ------------------ Helper ------------------
def emotion_to_strategy(label):
    if not label:
        return "neutral"
    low = {"sadness", "fear", "anger"}
    high = {"joy", "optimism", "love"}
    if label in low: return "short-first"
    if label in high: return "long-first"
    return "neutral"

def df_to_tasks(df):
    tasks = []
    for _, r in df.iterrows():
        # Safely extract and convert values
        hours = r.get("Hours", 0)
        minutes = r.get("Minutes", 0)
        try:
            hours = int(hours) if hours not in [None, ""] else 0
        except ValueError:
            hours = 0
        try:
            minutes = int(minutes) if minutes not in [None, ""] else 0
        except ValueError:
            minutes = 0

        duration_mins = hours * 60 + minutes

        # ✅ Correct column name for task name
        task_name = str(r.get("Task Name", "") or "").strip()

        task = {
            "Task": task_name if task_name else "Untitled Task",
            "Duration (mins)": duration_mins
        }
        tasks.append(task)
    return tasks


def make_events(tasks, start_dt, gap):
    evs = []
    now = start_dt
    for task in tasks:
        # Correct key lookups
        name = task.get("Task") or task.get("Task Name") or "Untitled Task"
        mins = int(task.get("Duration (mins)", 30))
        end = now + datetime.timedelta(minutes=mins)
        evs.append({
            "title": name.strip() if name else "Untitled Task",
            "start": now.strftime("%Y-%m-%dT%H:%M:%S"),
            "end": end.strftime("%Y-%m-%dT%H:%M:%S")
        })
        now = end + datetime.timedelta(minutes=gap)
    return evs


# ------------------ Step 4: Calendar Choice ------------------
st.markdown("---")
st.header("📅 Step 4 — Choose Calendar Type")
calendar_type = st.radio("Select calendar type:", ["Use Built-in Calendar", "Sync with Google Calendar"], horizontal=True)

# ------------------ Step 5: Generate ------------------
st.markdown("---")
st.header("✨ Step 5 — Generate Smart Schedule")

if st.button("🚀 Generate Smart Schedule"):
    task_list = df_to_tasks(st.session_state.tasks_df)
    if not task_list:
        st.warning("Add at least one valid task.")
    else:
        mood = st.session_state.detected_mood["label"] if st.session_state.detected_mood else None
        strategy = emotion_to_strategy(mood)
        if strategy == "long-first":
            task_list.sort(key=lambda x: -x[1])
            st.info("High energy — long tasks first.")
        elif strategy == "short-first":
            task_list.sort(key=lambda x: x.get("Priority", ""), reverse=True)
            st.info("Low energy — starting easy.")
        else:
            st.info("Neutral — default order.")

        start_dt = datetime.datetime.combine(datetime.date.today(), start_time)
        st.session_state.events = make_events(task_list, start_dt, break_min)
        st.success("✅ Schedule generated!")

# ------------------ Local Calendar ------------------
def show_local_calendar():
    st.subheader("📆 Local Calendar")
    if not st.session_state.events:
        st.warning("No events. Click Generate first.")
        return

    # Ensure titles exist and fix AM/PM display
    for e in st.session_state.events:
        if "title" not in e or not e["title"]:
            e["title"] = "Untitled Task"

    options = {
        "editable": True,
        "initialView": "timeGridDay",
        "slotMinTime": "06:00:00",
        "slotMaxTime": "23:00:00",
        "height": 650,
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek,timeGridDay"
        },
        # ✅ Force full AM/PM display in slot labels
        "slotLabelFormat": {
            "hour": "numeric",
            "minute": "2-digit",
            "hour12": True
        },
        # ✅ Make sure event titles are visible
        "eventDisplay": "block",
        "eventTimeFormat": {
            "hour": "numeric",
            "minute": "2-digit",
            "hour12": True
        }
    }

    cal_state = calendar(events=st.session_state.events, options=options, key="cal_main")
    if cal_state and "events" in cal_state:
        st.session_state.events = cal_state["events"]

    st.download_button(
        "⬇️ Export as .ics",
        data=Calendar(events=[
            Event(name=e["title"], begin=e["start"], end=e["end"])
            for e in st.session_state.events
        ]).serialize(),
        file_name="mindsync_schedule.ics",
        mime="text/calendar"
    )


# ------------------ Google Calendar Sync ------------------
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_gcal_service():
    creds = None
    if os.path.exists("token.pkl"):
        with open("token.pkl", "rb") as t:
            creds = pickle.load(t)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=8080)
        with open("token.pkl", "wb") as t:
            pickle.dump(creds, t)
    service = build("calendar", "v3", credentials=creds)
    return service

def show_google_sync():
    st.subheader("🌐 Google Calendar Sync")
    if not st.session_state.events:
        st.warning("Generate events first.")
        return

    if st.button("🔐 Authorize Google"):
        try:
            service = get_gcal_service()
            st.session_state["gcal_service"] = service
            st.success("✅ Authorized successfully!")
        except Exception as e:
            st.error(f"Authorization failed: {e}")

    if "gcal_service" in st.session_state:
        if st.button("☁️ Sync to Google Calendar"):
            service = st.session_state["gcal_service"]
            count = 0
            for ev in st.session_state.events:
                event = {
                    "summary": ev["title"],
                    "start": {"dateTime": ev["start"], "timeZone": timezone},
                    "end": {"dateTime": ev["end"], "timeZone": timezone},
                }
                service.events().insert(calendarId="primary", body=event).execute()
                count += 1
            st.success(f"✅ Synced {count} events to Google Calendar!")

# ------------------ Step 6: Display ------------------
st.markdown("---")
st.header("🧭 Step 6 — View / Sync Schedule")

if calendar_type == "Use Built-in Calendar":
    show_local_calendar()
else:
    show_google_sync()

# ------------------ Footer ------------------
with st.expander("Debug JSON"):
    st.json(st.session_state.events)

st.markdown("---")
st.caption("🚀 Next: Add login/signup + database + UI polish.")
