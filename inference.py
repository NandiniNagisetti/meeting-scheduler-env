# inference.py
import random

# simple env simulation
schedule = [0] * 10
task_name = "meeting_scheduler"

print(f"[START] task={task_name}", flush=True)

total_reward = 0
num_steps = 0

for step in range(1, 11):
    # find first free slot
    try:
        slot = schedule.index(0)
        schedule[slot] = 1
        reward = 1  # reward for successful scheduling
    except ValueError:
        slot = -1
        reward = 0  # no free slot

    total_reward += reward
    num_steps += 1

    print(f"[STEP] step={step} reward={reward}", flush=True)

final_score = total_reward / num_steps
print(f"[END] task={task_name} score={final_score:.2f} steps={num_steps}", flush=True)
