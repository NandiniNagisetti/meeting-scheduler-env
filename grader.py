def grade(env):
    total_slots = len(env.schedule)
    filled = sum(env.schedule)

    efficiency = filled / total_slots

    # Priority score
    max_priority = sum([r.priority for r in env.requests])
    achieved_priority = sum([
        r.priority for i, r in enumerate(env.requests)
        if i < len(env.schedule) and env.schedule[r.time] == 1
    ])

    if max_priority == 0:
        priority_score = 0
    else:
        priority_score = achieved_priority / max_priority

    # Final score
    score = (0.5 * efficiency) + (0.5 * priority_score)

    return round(score, 3)
