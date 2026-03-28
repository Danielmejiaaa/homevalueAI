from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
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

    @field_validator("area")
    @classmethod
    def validate_area(cls, value):
        if value <= 0:
            raise ValueError("El área debe ser mayor que 0.")
        return value

    @field_validator("rooms")
    @classmethod
    def validate_rooms(cls, value):
        if value <= 0:
            raise ValueError("El número de habitaciones debe ser mayor que 0.")
        return value

    @field_validator("bathrooms")
    @classmethod
    def validate_bathrooms(cls, value):
        if value < 1:
            raise ValueError("El número de baños debe ser al menos 1.")
        return value

    @field_validator("parking")
    @classmethod
    def validate_parking(cls, value):
        if value < 0:
            raise ValueError("El número de parqueaderos no puede ser negativo.")
        return value

    @field_validator("age")
    @classmethod
    def validate_age(cls, value):
        if value < 0:
            raise ValueError("La antigüedad no puede ser negativa.")
        return value

    @field_validator("location")
    @classmethod
    def validate_location(cls, value):
        if not value.strip():
            raise ValueError("La ubicación no puede estar vacía.")
        return value.strip()

@app.get("/")
def read_root():
    return {"message": "Prediction service running"}

@app.post("/predict")
def predict(data: HouseData):
    try:
        price = (
            float(data.area) * 1000
            + int(data.rooms) * 50000
            + int(data.bathrooms) * 30000
            + int(data.parking) * 20000
            - int(data.age) * 1000
        )

        return {"predicted_price": int(price)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))