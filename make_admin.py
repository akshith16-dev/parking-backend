from database import SessionLocal
from models.user import User

db = SessionLocal()
user = db.query(User).filter(User.username == "akshith").first()
user.role = "admin"
db.commit()
print("Done! You are now admin.")
db.close()