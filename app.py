import gradio as gr
import random
import re
import time
from pydantic import BaseModel
from typing import List, Optional
import speech_recognition as sr

# =========================
# MODELS
# =========================

class MeetingRequest(BaseModel):
    name: str
    time: int
    priority: int
    duration: int = 1
    participants: int = 1

class Observation(BaseModel):
    schedule: List[int]
    current_request: Optional[MeetingRequest]

class Action(BaseModel):
    action_type: str

class Reward(BaseModel):
    score: float

# =========================
# ENVIRONMENT
# =========================

class MeetingEnv:
    def __init__(self):
        self.reset()

    def reset(self):
        self.schedule = [0] * 10
        self.prev_schedule = self.schedule.copy()
        self.history = []

        self.requests = [
            MeetingRequest(
                name=f"Meeting {i}",
                time=random.randint(0, 9),
                priority=random.randint(1, 5),
                duration=random.randint(1, 3),
                participants=random.randint(1, 10),
            )
            for i in range(6)
        ]

        self.index = 0
        self.total_reward = 0
        return self.state()

    def state(self):
        if self.index < len(self.requests):
            return Observation(
                schedule=self.schedule,
                current_request=self.requests[self.index]
            )
        return Observation(schedule=self.schedule, current_request=None)

    def step(self, action: Action):
        request = self.requests[self.index]
        self.prev_schedule = self.schedule.copy()

        conflict = any(
            self.schedule[t] == 1
            for t in range(request.time, min(10, request.time + request.duration))
        )

        success = False
        if action.action_type == "schedule" and not conflict:
            for t in range(request.time, min(10, request.time + request.duration)):
                self.schedule[t] = 1
            success = True

        priority_bonus = request.priority * 0.2 if success else 0
        conflict_penalty = -0.5 if conflict else 0

        reward = (1 + priority_bonus) if success else -0.5
        reward = max(0.0, min(1.0, reward / 3))

        breakdown = f"""
Reward Breakdown:
+ Priority bonus: {round(priority_bonus,2)}
- Conflict penalty: {round(conflict_penalty,2)}
"""

        self.history.append({
            "meeting": request.name,
            "action": action.action_type,
            "reward": round(reward, 2)
        })

        self.index += 1
        done = self.index >= len(self.requests)

        if done:
            efficiency = sum(self.schedule) / len(self.schedule)
            reward += efficiency * 0.5

        self.total_reward += reward

        return self.state(), Reward(score=reward), done, breakdown

# =========================
# FAKE GOOGLE CALENDAR
# =========================

def push_to_calendar(start, duration):
    time.sleep(1.5)
    return f"🔄 Syncing with Google Calendar...\n\n✅ Event pushed at {start}:00"

# =========================
# GLOBAL ENV
# =========================

env = MeetingEnv()

# =========================
# AI + NLP
# =========================

def find_best_slot(schedule, duration):
    for start in range(10):
        end = start + duration
        if end > len(schedule):
            continue
        if not any(schedule[t] == 1 for t in range(start, end)):
            return start
    return None

def parse_voice(text):
    text = text.lower()
    duration = 1
    priority = 3

    if "2" in text:
        duration = 2
    elif "3" in text:
        duration = 3

    if "high" in text:
        priority = 5
    elif "low" in text:
        priority = 1

    return duration, priority

def ai_decision(obs):
    r = obs.current_request
    if not r:
        return "done"
    return "schedule" if r.priority >= 3 else "reject"

# =========================
# XAI
# =========================

def explain_decision(obs):
    if not obs.current_request:
        return "No decision"

    r = obs.current_request
    reasons = []

    if r.priority >= 4:
        reasons.append("🔥 High priority")

    if r.duration > 2:
        reasons.append("⏳ Long meeting")

    if any(obs.schedule[t] == 1 for t in range(r.time, min(10, r.time + r.duration))):
        reasons.append("⚠️ Conflict detected")

    if not reasons:
        reasons.append("👍 Safe to schedule")

    return "\n".join(reasons)

# =========================
# UI RENDERING
# =========================

def render_calendar(schedule, request):
    html = """
    <style>
    .slot {
        margin:5px;
        padding:12px;
        color:white;
        border-radius:8px;
        transition:0.3s;
    }
    .slot:hover {
        transform:scale(1.2);
    }
    </style>
    """
    html += "<h3>📅 Calendar</h3><div style='display:flex;'>"

    for i, slot in enumerate(schedule):
        color = "#2ecc71" if slot == 0 else "#e74c3c"
        if request and request.time <= i < request.time + request.duration:
            color = "#f1c40f"
        html += f"<div class='slot' style='background:{color}'>{i}</div>"

    html += "</div><p>🟢 Free | 🔴 Busy | 🟡 Proposed</p>"
    return html

def render_heatmap(schedule):
    html = "<h3>📊 Heatmap</h3><div style='display:flex;'>"
    for s in schedule:
        color = "#2ecc71" if s == 0 else "#e74c3c"
        html += f"<div style='width:25px;height:25px;margin:3px;background:{color}'></div>"
    html += "</div>"
    return html

# =========================
# ACTIONS
# =========================

def step(action_type):
    global env
    obs_before = env.state()
    ai_act = ai_decision(obs_before)

    obs, reward, done, breakdown = env.step(Action(action_type=action_type))

    calendar_msg = ""
    if action_type == "schedule":
        r = obs_before.current_request
        calendar_msg = push_to_calendar(r.time, r.duration)

    return (
        render_calendar(env.prev_schedule, obs_before.current_request),
        render_calendar(obs.schedule, obs.current_request),
        float(reward.score),
        explain_decision(obs_before) + "\n\n" + calendar_msg,
        f"👤 You: {action_type} | 🤖 AI: {ai_act}",
        breakdown,
        render_heatmap(env.schedule)
    )

def auto_schedule():
    global env
    obs = env.state()
    r = obs.current_request

    if not r:
        return ["Done"] * 7

    best = find_best_slot(obs.schedule, r.duration)

    if best is not None:
        r.time = best
        return step("schedule")
    else:
        return step("reject")

def voice_schedule(text):
    global env
    obs = env.state()
    r = obs.current_request

    if not r:
        return ["Done"] * 7

    duration, priority = parse_voice(text)
    r.duration = duration
    r.priority = priority

    return auto_schedule()

def audio_schedule(audio_file):
    if audio_file is None:
        return ["No audio uploaded"] * 7

    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
    except Exception as e:
        text = f"Could not understand audio: {str(e)}"

    return voice_schedule(text)

def reset():
    global env
    env = MeetingEnv()
    obs = env.reset()

    return (
        "",
        render_calendar(obs.schedule, obs.current_request),
        0.0,
        "Reset",
        "",
        "",
        render_heatmap(obs.schedule)
    )

# =========================
# UI
# =========================

with gr.Blocks() as demo:
    gr.Markdown("# 🏆 Explainable AI Smart Scheduler")

    with gr.Row():
        btn_schedule = gr.Button("📌 Schedule")
        btn_reject = gr.Button("❌ Reject")
        btn_auto = gr.Button("🤖 Auto AI")
        btn_reset = gr.Button("🔄 Reset")

    voice_input = gr.Textbox(label="🎤 Voice (type command)")
    voice_btn = gr.Button("🎤 Run Voice")

    audio_input = gr.Audio(label="🎤 Upload Voice Command", type="filepath")
    audio_btn = gr.Button("🎤 Run Audio")

    before_box = gr.HTML(label="Before")
    after_box = gr.HTML(label="After")
    reward_box = gr.Number(label="Reward")
    explain_box = gr.Markdown(label="AI Reasoning")
    compare_box = gr.Markdown(label="Human vs AI")
    breakdown_box = gr.Markdown(label="Reward Breakdown")
    heatmap_box = gr.HTML()

    btn_schedule.click(lambda: step("schedule"),
        outputs=[before_box, after_box, reward_box, explain_box, compare_box, breakdown_box, heatmap_box])

    btn_reject.click(lambda: step("reject"),
        outputs=[before_box, after_box, reward_box, explain_box, compare_box, breakdown_box, heatmap_box])

    btn_auto.click(auto_schedule,
        outputs=[before_box, after_box, reward_box, explain_box, compare_box, breakdown_box, heatmap_box])

    voice_btn.click(voice_schedule,
        inputs=[voice_input],
        outputs=[before_box, after_box, reward_box, explain_box, compare_box, breakdown_box, heatmap_box])

    audio_btn.click(audio_schedule,
        inputs=[audio_input],
        outputs=[before_box, after_box, reward_box, explain_box, compare_box, breakdown_box, heatmap_box])

    btn_reset.click(reset,
        outputs=[before_box, after_box, reward_box, explain_box, compare_box, breakdown_box, heatmap_box])

demo.launch(server_name="0.0.0.0", server_port=7860)
