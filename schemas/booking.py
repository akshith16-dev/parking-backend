from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BookingBase(BaseModel):
    slot_id: int
    vehicle_number: str
    duration_hours: int

class BookingCreate(BookingBase):
    pass

class BookingResponse(BookingBase):
    id: int
    user_id: int
    booked_at: datetime
    status: str

    class Config:
        from_attributes = True
