from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

app = FastAPI()

# MongoDB Connection
MONGO_URI = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URI)
db = client["tunisia_app"]

# Define a Pydantic model for validation
class Place(BaseModel):
    name: str
    description: str
    location: str

# Add a new place
@app.post("/places/")
async def add_place(place: Place):
    result = await db.places.insert_one(place.dict())
    return {"message": "Place added", "id": str(result.inserted_id)}

# Get all places
@app.get("/places")
async def get_places():
    places = await db.places.find().to_list(100)
    return places

