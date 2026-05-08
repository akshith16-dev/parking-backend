from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class ParkingSlot(Base):
    __tablename__ = "parking_slots"

    id = Column(Integer, primary_key=True, index=True)
    slot_number = Column(String(10), unique=True, nullable=False)
    floor = Column(Integer, nullable=False)
    slot_type = Column(String(20), default='Car')
    available = Column(Boolean, default=True)
