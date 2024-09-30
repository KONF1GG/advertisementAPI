from pydantic import BaseModel
from datetime import datetime
from typing import Literal, Optional


class ItemId(BaseModel):
    id: int


class GetAdvertisement(BaseModel):
    id: int
    title: str
    description: str
    price: float
    author: str
    created_at: datetime


class CreateAdvertisement(BaseModel):
    title: str
    description: str
    price: float
    author: str


class UpdateAdvertisement(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None
    author: str | None = None


class StatusResponse(BaseModel):
    status: Literal['success', 'deleted']

class SearchAdvertisement(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    author: Optional[str] = None