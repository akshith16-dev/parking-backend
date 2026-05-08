from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.booking import Booking
from models.parking_slot import ParkingSlot
from schemas.booking import BookingCreate, BookingResponse
from models.user import User
from dependencies import get_current_user, get_current_admin

router = APIRouter(prefix="/bookings", tags=["bookings"])

@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    slot = db.query(ParkingSlot).filter(ParkingSlot.id == booking.slot_id).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")
    if not slot.available:
        raise HTTPException(status_code=400, detail="Slot is not available")
    
    new_booking = Booking(
        slot_id=booking.slot_id,
        user_id=current_user.id,
        vehicle_number=booking.vehicle_number,
        duration_hours=booking.duration_hours
    )
    db.add(new_booking)
    
    # Mark slot as unavailable
    slot.available = False
    
    db.commit()
    db.refresh(new_booking)
    return new_booking

@router.get("/", response_model=List[BookingResponse])
def get_all_bookings(db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    bookings = db.query(Booking).all()
    return bookings

@router.get("/me", response_model=List[BookingResponse])
def get_my_bookings(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    bookings = db.query(Booking).filter(Booking.user_id == current_user.id).all()
    return bookings

@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_booking(booking_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    if current_user.role != "admin" and booking.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to cancel this booking")
    
    booking.status = "Cancelled"
    
    # Free up the slot
    slot = db.query(ParkingSlot).filter(ParkingSlot.id == booking.slot_id).first()
    if slot:
        slot.available = True
        
    db.commit()
    return None
