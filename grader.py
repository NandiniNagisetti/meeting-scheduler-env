def safe_score(x):
    # force strictly between (0,1)
    if x <= 0:
        return 0.1
    if x >= 1:
        return 0.9
    return float(x)


def grade_easy(total_reward):
    raw = total_reward / 10
    return safe_score(raw)


def grade_medium(total_reward):
    raw = (total_reward + 2) / 12
    return safe_score(raw)


def grade_hard(total_reward):
    raw = (total_reward + 3) / 15
    return safe_score(raw)
