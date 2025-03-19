#run using uvicorn main:app --reload
#http://127.0.0.1:8000

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models import User
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from decimal import Decimal
import logging
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
import httpx  

logging.basicConfig(
    filename="user_service.log",  # Store logs in a file
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("UserService")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", 
    "http://frontend:5500"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
async def read_root():
    logger.info("Root endpoint accessed.")
    return {"message": "Hello, FastAPI with PostgreSQL!"}

#ensure that all inputs are of required datatype
class UserCreate(BaseModel):
    email: str
    password: str
    username: str
    balance: Decimal

class LoginRequest(BaseModel):
    username: str
    password: str

class BookingRequest(BaseModel):
    event_id: int
    user_id: int
    price: int
    ticket_count: int

#handle get at users
@app.get("/users/")
async def get_users(db: AsyncSession = Depends(get_db)):
    logger.info("Fetching all users.")
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users

@app.post("/login/")
async def login(user: LoginRequest, db: AsyncSession = Depends(get_db)):
    logger.info(f"Login attempt for username: {user.username}, password: {user.password}")
    try:
        result = await db.execute(select(User).where(User.username == user.username))
        db_user = result.scalars().first()
        if not db_user or db_user.password != user.password:  
            raise HTTPException(status_code=401, detail="Invalid username or password")

        logger.info(f"User {user.username} logged in successfully.")
        return {"username": db_user.username, "balance": db_user.balance, "id": db_user.id}
    
    except HTTPException as http_err:
        logger.error(f"HTTP Exception: {http_err.detail}")
        raise http_err  

    except Exception as e:
        logger.exception(f"Unhandled exception occurred {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


# API Endpoint to Create a User
@app.post("/users/")
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    logger.info(f"Creating user: {user.username}")
    try:
        new_user = User(email=user.email, password=user.password, username=user.username, balance=user.balance)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        logger.info(f"User created successfully: {new_user.username}")
        return {
            "id": new_user.id,
            "email": new_user.email,
            "username": new_user.username,
            "balance": new_user.balance
        }
    except IntegrityError: 
        await db.rollback() 
        logger.error("User creation failed: Username or email already exists")
        raise HTTPException(status_code=400, detail="Username or email already exists")
    except Exception as e:
        await db.rollback()
        logger.error(f"Unexpected error in user creation: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@app.get("/users/events/")
async def get_events():
    events_url = "http://event_service:8080/api/events" 
    logger.info("Fetching events from event service.")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(events_url)
            response.raise_for_status()  
            logger.info("Successfully retrieved events.")
            return response.json()  
    except httpx.HTTPStatusError as e:
        logger.error(f"Error retrieving events: {str(e)}")
        raise HTTPException(status_code=e.response.status_code, detail="Error retrieving events")
    except Exception as e:
        logger.error(f"Unexpected error retrieving events: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/users/bookings/")
async def create_booking(booking: BookingRequest, db: AsyncSession = Depends(get_db)):
    logger.info(f"Received booking request for user {booking.user_id} and event {booking.event_id}")
    # Step 1: Get User from Database
    result = await db.execute(select(User).where(User.id == booking.user_id))
    db_user = result.scalars().first()

    if not db_user:
        logger.warning("Booking failed: User not found.")
        raise HTTPException(status_code=404, detail="User not found")

    # Step 2: Check User Balance
    if db_user.balance < booking.price:
        logger.warning("Booking failed: Insufficient balance.")
        raise HTTPException(status_code=400, detail="Insufficient balance")

    # Step 3: Call Booking API to Create Booking
    try:
        async with httpx.AsyncClient() as client:
            logger.info(f"Calling booking API for user {booking.user_id}")
            booking_response = await client.post(
                "http://booking_service:5000/bookings", json=booking.dict()
            )
            booking_response.raise_for_status()
            booking_data = booking_response.json()
            logger.info(f"Booking successful, ID: {booking_data['booking_id']}")
    except httpx.HTTPStatusError as e:
        if e.response is not None:
            error_json = e.response.json()  # Get error response as dict
            error_message = error_json.get("error", str(error_json))  # Extract error field if it exists
        else:
            error_message = "Booking API error"
    
        logger.error(f"Booking API error: {str(e)}")
        raise HTTPException(status_code=e.response.status_code, detail=error_message)
    except Exception as e:
        logger.error(f"Unexpected error in booking process: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

    # Step 4: Deduct Balance After Successful Booking
    db_user.balance -= booking.price
    await db.commit()

    logger.info(f"Updated balance for user {db_user.id} after booking.")
    return {
        "message": "Booking successful",
        "booking_id": booking_data["booking_id"],
        "remaining_balance": db_user.balance
    }