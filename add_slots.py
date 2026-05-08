from database import SessionLocal
from models.parking_slot import ParkingSlot

db = SessionLocal()

slots = []

# Ground Floor - Trucks (5 slots)
for i in range(1, 6):
    slots.append(ParkingSlot(slot_number=f"G-{i:02d}", floor=0, slot_type="Truck"))

# Floor 1 - Cars (10 slots)
for i in range(1, 11):
    slots.append(ParkingSlot(slot_number=f"A-{i:02d}", floor=1, slot_type="Car"))

Floor 2 - Bikes (10 slots)
for i in range(1, 11):
    slots.append(ParkingSlot(slot_number=f"B-{i:02d}", floor=2, slot_type="Bike"))

# Floor 3 - EV (5 slots)
for i in range(1, 6):
    slots.append(ParkingSlot(slot_number=f"C-{i:02d}", floor=3, slot_type="EV"))

db.add_all(slots)
db.commit()
db.close()

print("✓ 30 slots added successfully!")
print("  Ground Floor: 5 Truck slots")
print("  Floor 1: 10 Car slots")
print("  Floor 2: 10 Bike slots")
print("  Floor 3: 5 EV slots")