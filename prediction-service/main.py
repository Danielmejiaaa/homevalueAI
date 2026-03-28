from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class HouseData(BaseModel):
    area: float
    rooms: int
    bathrooms: int
    parking: int
    age: int
    location: str

@app.get("/")
def read_root():
    return {"message": "Prediction service running"}

@app.post("/predict")
def predict(data: HouseData):
    price = (
        data.area * 1000 +
        data.rooms * 50000 +
        data.bathrooms * 30000 +
        data.parking * 20000 -
        data.age * 1000
    )

    return {"predicted_price": int(price)}