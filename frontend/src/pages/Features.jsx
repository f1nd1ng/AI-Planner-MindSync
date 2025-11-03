import { useEffect, useRef, useState } from "react";
import "../styles.css";
import CalendarView from "../components/CalendarView";
import { apiDetectMood, apiGenerateSchedule } from "../api/client";

export default function Features() {
  const [moodText, setMoodText] = useState("");
  const [moodResult, setMoodResult] = useState(null);
  const [tasks, setTasks] = useState([
  ]);
  const [settings, setSettings] = useState({
    start: "09:00",
    breakMin: 10,
    tz: "Asia/Kolkata",
    calType: "local",
  });
  const [events, setEvents] = useState([]);

  // reveal-on-scroll
  const sectionsRef = useRef([]);
  useEffect(() => {
    const io = new IntersectionObserver(
      (entries) =>
        entries.forEach((e) => e.isIntersecting && e.target.classList.add("in-view")),
      { threshold: 0.25 }
    );
    sectionsRef.current.forEach((el) => el && io.observe(el));
    return () => io.disconnect();
  }, []);
  const attach = (el, i) => (sectionsRef.current[i] = el);

  // ===== API actions =====
  const handleDetectMood = async () => {
    try {
      const res = await apiDetectMood(moodText || "");
      setMoodResult(res); // {label, friendly, emoji, confidence}
    } catch (err) {
      console.error("Detect mood failed:", err);
      setMoodResult({ label: "neutral", friendly: "Neutral", emoji: "🙂", confidence: 0 });
      alert("Could not detect mood. Check API logs.");
    }
  };

  const addRow = () => setTasks((t) => [...t, { name: "", hrs: 0, mins: 0 }]);
  const updateTask = (i, key, val) =>
    setTasks((list) =>
      list.map((t, idx) => (idx === i ? { ...t, [key]: key === "name" ? val : +val } : t))
    );
  const removeTask = (i) => setTasks((list) => list.filter((_, idx) => idx !== i));

  const handleGenerate = async () => {
    try {
      const payload = {
        tasks: tasks.map((t) => ({
          name: t.name || "Untitled Task",
          hours: Number(t.hrs || 0),
          minutes: Number(t.mins || 0),
        })),
        mood_label: (moodResult?.label || "neutral").toLowerCase(),
        start_time: settings.start,
        break_min: Number(settings.breakMin || 0),
      };
      const res = await apiGenerateSchedule(payload);
      setEvents(res?.events || []);
    } catch (err) {
      console.error("Generate schedule failed:", err);
      setEvents([]);
      alert("Could not generate schedule. Check API logs.");
    }
  };

  return (
    <div className="flow-wrap">
      <div className="site-container flow-lane spacious">
        {/* 1 — UI left / Image right */}
        <section ref={(el) => attach(el, 0)} className="flow-section">
          <div className="panel ui-card">
            <h2 className="flow-title" style={{fontFamily: "'Times New Roman', serif",
    fontSize: 40,}}> Emotional check-in</h2>
            <p className="muted">Describe how you feel — we’ll map the energy of your day.</p>
            <textarea
              className="demo-textarea"
              placeholder="I'm a bit anxious but excited to finish the deck…"
              value={moodText}
              onChange={(e) => setMoodText(e.target.value)}
            />
            <div className="row">
              <button className="btn primary" onClick={handleDetectMood}>
                Detect mood
              </button>
              {moodResult && (
                <div className="mood-chip">
                  {moodResult.emoji} <b>{moodResult.friendly}</b>&nbsp;
                  ({Math.round((moodResult.confidence || 0) * 100)}%)
                </div>
              )}
            </div>
            <ul style={{ listStyle: "none", paddingLeft: 0 }}>
            <li
                style={{
                fontFamily: "'Times New Roman', serif",
                fontSize: "16px",
                fontWeight: "200",   // lighter text
                lineHeight: "1.4",
                color: "#0F3B2E" 
                }}
            >
                Just enter a short phrase, and we will check right up on you :)
            </li>
            </ul>
          </div>

          <div className="panel art-card">
            <div className="art-stage">
              <img className="art-img" src="/assets/1.png" alt="Emotion Check-in" />
            </div>
          </div>
        </section>

        {/* 2 — Image left / UI right */}
        <section ref={(el) => attach(el, 1)} className="flow-section alt">
          <div className="panel art-card">
            <div className="art-stage">
              <img className="art-img" src="/assets/2.png" alt="Smart Schedule" />
            </div>
          </div>

          <div className="panel ui-card">
            <h2 className="flow-title" style={{fontFamily: "'Times New Roman', serif",
    fontSize: 40,}}>Tasks to get done</h2>
            <p className="muted">Fast task entry with rough durations.</p>

            <div className="task-table">
              <div className="t-head">
                <div>Task Name</div>
                <div>Hrs</div>
                <div>Mins</div>
                <div />
              </div>
              {tasks.map((t, i) => (
                <div className="t-row" key={i}>
                  <input
                    value={t.name}
                    placeholder="Task…"
                    onChange={(e) => updateTask(i, "name", e.target.value)}
                  />
                  <input
                    type="number"
                    min={0}
                    value={t.hrs}
                    onChange={(e) => updateTask(i, "hrs", e.target.value)}
                  />
                  <input
                    type="number"
                    min={0}
                    value={t.mins}
                    onChange={(e) => updateTask(i, "mins", e.target.value)}
                  />
                  <button className="icon-btn" onClick={() => removeTask(i)} title="Remove">
                    ✕
                  </button>
                </div>
              ))}
              <button className="btn ghost small" onClick={addRow}>
                + Add row
              </button>
            </div>

            <ul style={{ listStyle: "none", paddingLeft: 0 }}>
            <li
                style={{
                fontFamily: "'Times New Roman', serif",
                fontSize: "16px",
                fontWeight: "200",   // lighter text
                lineHeight: "1.4",
                color: "#0F3B2E" 
                }}
            >
                Use the + button to add new tasks and the time you need to complete it. 
            </li>
            </ul>
          </div>
        </section>

        {/* 3 — UI left / Image right */}
        <section ref={(el) => attach(el, 2)} className="flow-section">
          <div className="panel ui-card">
            <h2 className="flow-title" style={{fontFamily: "'Times New Roman', serif",
    fontSize: 40,}}>Customize your day</h2>
            <div className="grid-3">
              <div className="form-field">
                <label>Start time</label>
                <select
                  value={settings.start}
                  onChange={(e) => setSettings((s) => ({ ...s, start: e.target.value }))}
                >
                    <option>05:00</option>
                    <option>06:00</option>
                    <option>07:00</option>
                    <option>08:00</option>
                    <option>09:00</option>
                    <option>10:00</option>
                    <option>11:00</option>
                    <option>12:00</option>
                    <option>13:00</option>
                    <option>14:00</option>
                    <option>15:00</option>
                    <option>16:00</option>
                    <option>17:00</option>
                    <option>18:00</option>
                    <option>19:00</option>
                    <option>20:00</option>
                    <option>21:00</option>
                    <option>22:00</option>
                    <option>23:00</option>
                </select>
              </div>
              <div className="form-field">
                <label>Break (mins)</label>
                <input
                  type="number"
                  value={settings.breakMin}
                  onChange={(e) => setSettings((s) => ({ ...s, breakMin: +e.target.value }))}
                />
              </div>
              <div className="form-field">
                <label>Timezone</label>
                <select
                  value={settings.tz}
                  onChange={(e) => setSettings((s) => ({ ...s, tz: e.target.value }))}
                >
                  <option>Asia/Kolkata</option>
                  <option>UTC</option>
                  <option>US/Eastern</option>
                  <option>Europe/London</option>
                </select>
              </div>
            </div>
            <ul style={{ listStyle: "none", paddingLeft: 0 }}>
            <li
                style={{
                fontFamily: "'Times New Roman', serif",
                fontSize: "16px",
                fontWeight: "200",   // lighter text
                lineHeight: "1.4",
                color: "#0F3B2E" 
                }}
            >
                Just enter the amount of time you wanna rest between each task for increased efficiency.
            </li>
            </ul>
          </div>

          <div className="panel art-card">
            <div className="art-stage">
              <img className="art-img" src="/assets/3.png" alt="Calendar Sync" />
            </div>
          </div>
        </section>

        {/* 4 — Image left / UI right */}
        <section ref={(el) => attach(el, 3)} className="flow-section alt">
          <div className="panel art-card">
            <div className="art-stage">
              <img className="art-img" src="/assets/4.png" alt="Schedule Preview" />
            </div>
          </div>

          <div className="panel ui-card">
            <h2 className="flow-title" style={{fontFamily: "'Times New Roman', serif",
    fontSize: 40,}}>Choose calendar type</h2>
            <div className="radio-row">
              <label>
                <input
                  type="radio"
                  name="cal"
                  style={{fontFamily: "'Times New Roman', serif",
                    fontSize: 20,}}
                  checked={settings.calType === "local"}
                  onChange={() => setSettings((s) => ({ ...s, calType: "local" }))}
                />
                &nbsp;Use built-in calendar
              </label>
              <label>
                <input
                  type="radio"
                  name="cal"
                  checked={settings.calType === "google"}
                  onChange={() => setSettings((s) => ({ ...s, calType: "google" }))}
                />
                &nbsp;Sync with Google Calendar
              </label>
            </div>
            <ul className="bullets" style={{fontFamily: "'Times New Roman', serif",
                    fontSize: 20,}}>
              <li>Local preview calendar</li>
              <li>One-click export (.ics)</li>
            </ul>
          </div>
        </section>

        {/* 5 — Generate + Preview (merged into a single full-width block) */}
        <section ref={(el) => attach(el, 4)} className="flow-section full">
          <div className="panel ui-card full-card">
            <h2 className="flow-title">✨ Generate smart schedule</h2>
            <p className="muted">
              We’ll order tasks based on energy & add realistic buffers.
            </p>

            <button className="btn primary" onClick={handleGenerate}>
              Generate schedule
            </button>

            <ul className="bullets">
              <li>Energy-aware ordering</li>
              <li>Editable later</li>
            </ul>

            <h3 className="flow-sub" style={{ marginTop: "1.5rem" }}>
              Preview
            </h3>

            {/* Full width calendar below the button */}
            <div className="calendar-block">
              <CalendarView events={events} />
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}
