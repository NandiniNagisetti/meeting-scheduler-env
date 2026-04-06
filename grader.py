def grade(schedule):
    filled_slots = sum(schedule)
    return filled_slots / len(schedule)
