from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from routers import auth, slots, bookings
from startup import init_db
init_db()  # Add this line after Base.metadata.create_all
# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Vehicle Parking Management API")

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="https://parking-frontend.*\\.vercel\\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(slots.router)
app.include_router(bookings.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Vehicle Parking Management API"}
