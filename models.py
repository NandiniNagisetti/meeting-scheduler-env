from pydantic import BaseModel
from typing import List, Optional


class Participant(BaseModel):
    name: str
    availability: List[int]  # 10 slots (1 = free, 0 = busy)
    preferred_times: List[int]  # soft preference


class MeetingRequest(BaseModel):
    name: str
    duration: int
    participants: List[Participant]
    priority: int
    deadline: int  # latest acceptable start time
    is_recurring: bool = False


class Observation(BaseModel):
    global_schedule: List[int]
    current_request: Optional[MeetingRequest]


class Action(BaseModel):
    action_type: str  # "schedule" or "reject"
    start_time: Optional[int] = None


class Reward(BaseModel):
    score: float
