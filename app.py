import gradio as gr
from env import MeetingEnv
from models import Action

env = MeetingEnv()
obs = env.reset()

def take_action(action_type):
    global obs
    obs, reward, done, _ = env.step(Action(action_type=action_type))
    return str(obs), reward.score, done

def reset():
    global obs
    obs = env.reset()
    return str(obs), 0, False

with gr.Blocks() as demo:
    gr.Markdown("# 📅 Meeting Scheduler AI")

    output = gr.Textbox(label="Observation", lines=8)
    reward_box = gr.Number(label="Reward")
    done_box = gr.Checkbox(label="Done")

    with gr.Row():
        schedule_btn = gr.Button("📌 Schedule")
        reject_btn = gr.Button("❌ Reject")
        reset_btn = gr.Button("🔄 Reset")

    schedule_btn.click(lambda: take_action("schedule"), outputs=[output, reward_box, done_box])
    reject_btn.click(lambda: take_action("reject"), outputs=[output, reward_box, done_box])
    reset_btn.click(reset, outputs=[output, reward_box, done_box])

demo.launch()
