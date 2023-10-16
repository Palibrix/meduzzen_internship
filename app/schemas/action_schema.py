from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class ActionType(Enum):
    request = "request"
    invite = "invite"


class ActionSchema(BaseModel):
    action: ActionType


class Action(ActionSchema):
    action_id: int = Field(..., gt=0)
    user_id: int = Field(..., gt=0)
    company_id: int = Field(..., gt=0)


class ActionListResponse(BaseModel):
    actions: List[Action]
