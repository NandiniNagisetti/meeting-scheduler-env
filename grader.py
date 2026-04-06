def grade(schedule, total_reward):
    efficiency = sum(schedule) / len(schedule)

    # Normalize reward (rough scaling)
    normalized_reward = max(0, min(1, total_reward / 10))

    return 0.5 * efficiency + 0.5 * normalized_reward
