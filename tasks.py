def get_tasks():
    return [
        {
            "id": "easy",
            "description": "Schedule a meeting in a free slot",
            "grader": grade_easy
        },
        {
            "id": "medium",
            "description": "Avoid scheduling conflict",
            "grader": grade_medium
        },
        {
            "id": "hard",
            "description": "Optimize multiple meeting scheduling",
            "grader": grade_hard
        }
    ]


# ✅ graders MUST be separate functions
def grade_easy(output, state):
    if "scheduled" in str(output).lower():
        return 1.0
    return 0.0


def grade_medium(output, state):
    if "conflict" not in str(output).lower():
        return 1.0
    return 0.0


def grade_hard(output, state):
    if isinstance(output, str) and len(output) > 5:
        return 1.0
    return 0.0
