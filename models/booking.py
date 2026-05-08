from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database import Base
import datetime

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    slot_id = Column(Integer, ForeignKey("parking_slots.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    vehicle_number = Column(String(15), nullable=False)
    booked_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    duration_hours = Column(Integer, nullable=False)
    status = Column(String(20), default='Active')
