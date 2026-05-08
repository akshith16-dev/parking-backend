from pydantic import BaseModel
from typing import Optional

class ParkingSlotBase(BaseModel):
    slot_number: str
    floor: int
    slot_type: Optional[str] = 'Car'
    available: Optional[bool] = True

class ParkingSlotCreate(ParkingSlotBase):
    pass

class ParkingSlotUpdate(BaseModel):
    slot_number: Optional[str] = None
    floor: Optional[int] = None
    slot_type: Optional[str] = None
    available: Optional[bool] = None

class ParkingSlotResponse(ParkingSlotBase):
    id: int

    class Config:
        from_attributes = True
