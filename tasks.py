from models import MeetingRequest

def get_tasks():
    return {
        "easy": {
            "description": "Schedule all meetings without conflicts",
            "requests": [
                MeetingRequest(name="A", time=1, priority=1),
                MeetingRequest(name="B", time=3, priority=2),
            ]
        },
        "medium": {
            "description": "Schedule high priority meetings first",
            "requests": [
                MeetingRequest(name="A", time=1, priority=5),
                MeetingRequest(name="B", time=1, priority=2),
                MeetingRequest(name="C", time=4, priority=3),
            ]
        },
        "hard": {
            "description": "Optimize schedule for maximum priority + efficiency",
            "requests": [
                MeetingRequest(name="A", time=2, priority=5),
                MeetingRequest(name="B", time=2, priority=4),
                MeetingRequest(name="C", time=5, priority=3),
                MeetingRequest(name="D", time=7, priority=2),
            ]
        }
    }
