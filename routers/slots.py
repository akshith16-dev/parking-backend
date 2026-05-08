from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.parking_slot import ParkingSlot
from schemas.parking_slot import ParkingSlotCreate, ParkingSlotResponse, ParkingSlotUpdate
from models.user import User
from dependencies import get_current_user, get_current_admin

router = APIRouter(prefix="/slots", tags=["slots"])

@router.get("/", response_model=List[ParkingSlotResponse])
def get_slots(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    slots = db.query(ParkingSlot).all()
    return slots

@router.post("/", response_model=ParkingSlotResponse, status_code=status.HTTP_201_CREATED)
def create_slot(slot: ParkingSlotCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    db_slot = db.query(ParkingSlot).filter(ParkingSlot.slot_number == slot.slot_number).first()
    if db_slot:
        raise HTTPException(status_code=400, detail="Slot number already exists")
    new_slot = ParkingSlot(**slot.model_dump())
    db.add(new_slot)
    db.commit()
    db.refresh(new_slot)
    return new_slot

@router.get("/{slot_id}", response_model=ParkingSlotResponse)
def get_slot(slot_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    slot = db.query(ParkingSlot).filter(ParkingSlot.id == slot_id).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")
    return slot

@router.put("/{slot_id}", response_model=ParkingSlotResponse)
def update_slot(slot_id: int, slot: ParkingSlotUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    db_slot = db.query(ParkingSlot).filter(ParkingSlot.id == slot_id).first()
    if not db_slot:
        raise HTTPException(status_code=404, detail="Slot not found")
    
    update_data = slot.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_slot, key, value)
        
    db.commit()
    db.refresh(db_slot)
    return db_slot

@router.delete("/{slot_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_slot(slot_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    db_slot = db.query(ParkingSlot).filter(ParkingSlot.id == slot_id).first()
    if not db_slot:
        raise HTTPException(status_code=404, detail="Slot not found")
    
    db.delete(db_slot)
    db.commit()
    return None
