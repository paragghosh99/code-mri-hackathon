from pydantic import BaseModel
from typing import Literal,Optional


class Coordinates(BaseModel):
    x: int
    y: int


class ActionPlan(BaseModel):
    action: Literal["CLICK", "SCROLL", "SEARCH", "OPEN_FILE"]
    coordinates: Optional[Coordinates] = None
    reason: str