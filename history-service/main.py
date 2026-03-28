from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor

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

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="homevalue_db",
        user="postgres",
        password="postgres123",
        port="5432"
    )

@app.get("/")
def read_root():
    return {"message": "History service running"}

@app.get("/records")
def get_records():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("""
        SELECT id, area, rooms, bathrooms, parking, age, location, predicted_price, created_at
        FROM prediction_history
        ORDER BY id DESC
    """)
    records = cur.fetchall()

    cur.close()
    conn.close()

    return records

@app.post("/records")
def create_record(record: Record):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("""
        INSERT INTO prediction_history (area, rooms, bathrooms, parking, age, location, predicted_price)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id, area, rooms, bathrooms, parking, age, location, predicted_price, created_at
    """, (
        record.area,
        record.rooms,
        record.bathrooms,
        record.parking,
        record.age,
        record.location,
        record.predicted_price
    ))

    new_record = cur.fetchone()
    conn.commit()

    cur.close()
    conn.close()

    return {
        "message": "Record saved successfully",
        "record": new_record
    }