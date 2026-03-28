from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = FastAPI(title="HomeValue AI - History Service", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
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
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "homevalue_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres123"),
        port=os.getenv("DB_PORT", "5432"),
    )


@app.get("/")
def read_root():
    return {"message": "History service running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/records")
def get_records():
    try:
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

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving records: {str(e)}")


@app.post("/records")
def create_record(record: Record):
    try:
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

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving record: {str(e)}")