const API_BASE = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export async function apiDetectMood(text) {
  const r = await fetch(`${API_BASE}/detect_mood`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
  if (!r.ok) throw new Error(`detect_mood ${r.status}`);
  return r.json();
}

export async function apiGenerateSchedule({ tasks, mood_label, start_time, break_min }) {
  const r = await fetch(`${API_BASE}/generate_schedule`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ tasks, mood_label, start_time, break_min }),
  });
  if (!r.ok) throw new Error(`generate_schedule ${r.status}`);
  return r.json();
}
