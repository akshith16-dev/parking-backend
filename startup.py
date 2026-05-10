from database import SessionLocal, engine, Base
from models.parking_slot import ParkingSlot
from models.user import User

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Add slots only if empty
    if db.query(ParkingSlot).count() == 0:
        slots = []
        for i in range(1, 6):
            slots.append(ParkingSlot(slot_number=f"G-{i:02d}", floor=0, slot_type="Truck"))
        for i in range(1, 11):
            slots.append(ParkingSlot(slot_number=f"A-{i:02d}", floor=1, slot_type="Car"))
        for i in range(1, 11):
            slots.append(ParkingSlot(slot_number=f"B-{i:02d}", floor=2, slot_type="Bike"))
        for i in range(1, 6):
            slots.append(ParkingSlot(slot_number=f"C-{i:02d}", floor=3, slot_type="EV"))
        db.add_all(slots)
        db.commit()
        print("30 slots added!")

    db.close()

if __name__ == "__main__":
    init_db()