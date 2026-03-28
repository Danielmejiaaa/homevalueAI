from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Record(BaseModel):
    area: float
    rooms: int
    bathrooms: int
    parking: int
    age: int
    location: str
    predicted_price: int

records_db: List[Record] = []

@app.get("/")
def read_root():
    return {"message": "History service running"}

@app.get("/records")
def get_records():
    return records_db

@app.post("/records")
def create_record(record: Record):
    records_db.append(record)
    return {
        "message": "Record saved successfully",
        "record": record
    }