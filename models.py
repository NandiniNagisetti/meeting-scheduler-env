from pydantic import BaseModel
from typing import List, Optional

class MeetingRequest(BaseModel):
    name: str
    time: int   # 0–9 time slots
    priority: int  # 1–5

class Observation(BaseModel):
    schedule: List[int]
    current_request: Optional[MeetingRequest]

class Action(BaseModel):
    action_type: str  # "schedule" or "reject"

class Reward(BaseModel):
    score: float
