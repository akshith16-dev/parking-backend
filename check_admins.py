from database import SessionLocal
from models.user import User

db = SessionLocal()

admins = db.query(User).filter(User.role == "admin").all()

print("=== ADMINS ===")
for admin in admins:
    print(f"ID: {admin.id} | Username: {admin.username}")

print(f"\nTotal admins: {len(admins)}")

db.close()