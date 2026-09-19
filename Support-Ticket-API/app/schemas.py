from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class TicketCreate(BaseModel):
    customer_name: str = Field(min_length=2, max_length=100)
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=5)
    priority: Literal["low", "medium", "high"] = "medium"


class TicketResponse(BaseModel):
    id: int
    customer_name: str
    title: str
    description: str
    priority: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)