from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn
import httpx
import os
import re
import json

# Cargar variables de entorno desde .env
load_dotenv()

app = FastAPI(title="HomeValue AI - Predicción con IA", version="3.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()


class HouseData(BaseModel):
    area: float = Field(..., ge=10, le=1000, description="Área en metros cuadrados")
    rooms: int = Field(..., ge=1, le=10, description="Número de habitaciones")
    bathrooms: int = Field(..., ge=1, le=6, description="Número de baños")
    parking: int = Field(..., ge=0, le=5, description="Número de parqueaderos")
    age: int = Field(..., ge=0, le=100, description="Antigüedad en años")
    location: str = Field(..., min_length=1, description="Ubicación: norte, sur, centro, este, oeste")
    
    @field_validator("location")
    @classmethod
    def validate_location(cls, value):
        allowed_locations = {"norte", "sur", "centro", "este", "oeste"}
        normalized_value = value.strip().lower()

        if normalized_value not in allowed_locations:
            raise ValueError("La ubicación debe ser una de las siguientes: nrote, sur, centro, este u oeste. ")
        
        return normalized_value



class HousePricePredictor:
    def __init__(self):
        if GROQ_API_KEY:
            print("✅ Predictor IA inicializado con Llama 3.1 vía Groq")
        else:
            print("⚠️ No hay GROQ_API_KEY — usando fórmula de respaldo")

    async def predict_with_groq(self, data: HouseData) -> dict:
        prompt = f"""Eres un experto tasador inmobiliario de Cali, Colombia.

PRECIOS DE REFERENCIA EN CALI 2024-2025:
- Zona NORTE (Ciudad Jardín, Pance): $4.5M - $7M COP por m²
- Zona CENTRO (Granada, El Peñón): $4M - $5.5M COP por m²
- Zona OESTE (San Fernando): $3M - $4.5M COP por m²
- Zona ESTE (Villacolombia): $2M - $3M COP por m²
- Zona SUR (Meléndez, Siloé): $1.5M - $2.5M COP por m²
- Cada parqueadero suma entre 15M y 25M COP
- Cada año de antigüedad descuenta 0.8% del valor (máximo 30%)

VIVIENDA A TASAR:
- Área: {data.area} m²
- Habitaciones: {data.rooms}
- Baños: {data.bathrooms}
- Parqueaderos: {data.parking}
- Antigüedad: {data.age} años
- Zona: {data.location.upper()}

Responde SOLO con este JSON sin texto adicional:
{{
  "precio_estimado": <entero en COP>,
  "precio_minimo": <entero en COP>,
  "precio_maximo": <entero en COP>,
  "resumen_usuario": "<Una sola oración directa para el usuario>",
  "factores_clave": ["<factor 1>", "<factor 2>", "<factor 3>"]
}}"""

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "llama-3.1-8b-instant",
                    "max_tokens": 500,
                    "temperature": 0.1,
                    "messages": [
                        {
                            "role": "system",
                            "content": (
                                "Eres tasador inmobiliario de Cali Colombia. "
                                "Respondes SOLO con JSON válido. "
                                "Precios siempre en COP enteros."
                            ),
                        },
                        {
                            "role": "user",
                            "content": prompt,
                        },
                    ],
                },
            )

        if response.status_code != 200:
            raise Exception(f"Error Groq API: {response.status_code} - {response.text}")

        raw = response.json()["choices"][0]["message"]["content"]
        content = raw.strip()
        print(f"\n🤖 Respuesta de Llama:\n{content}\n")

        json_match = re.search(r"\{.*\}", content, re.DOTALL)
        if not json_match:
            raise Exception("El modelo no devolvió JSON válido")

        result = json.loads(json_match.group())
        price = int(result["precio_estimado"])

        if price < 80_000_000 or price > 10_000_000_000:
            print(f"⚠️ Precio fuera de rango ({price}), usando fórmula")
            return self.fallback_prediction(data)

        price_min = int(result["precio_minimo"])
        price_max = int(result["precio_maximo"])
        resumen = result.get("resumen_usuario", "")
        factores = result.get("factores_clave", [])

        return {
            "predicted_price": price,
            "price_min": price_min,
            "price_max": price_max,
            "confidence": 0.85,
            "model": "llama-3.1-8b-instant-groq",
            "summary": resumen,
            "key_factors": factores,
            "price_formatted": f"${price:,.0f} COP",
            "price_millions": round(price / 1_000_000, 1),
            "range": {
                "min": f"${price_min:,.0f} COP",
                "estimated": f"${price:,.0f} COP",
                "max": f"${price_max:,.0f} COP",
            },
        }

    def fallback_prediction(self, data: HouseData) -> dict:
        precio_m2 = {
            "norte": 4_500_000,
            "centro": 4_000_000,
            "este": 3_000_000,
            "oeste": 2_800_000,
            "sur": 2_500_000,
        }

        m2_val = precio_m2.get(data.location.lower(), 3_000_000)
        base = data.area * m2_val
        subtotal = (
            base
            + data.rooms * 12_000_000
            + data.bathrooms * 10_000_000
            + data.parking * 15_000_000
        )
        descuento = min(data.age * 0.008, 0.30)
        price = max(subtotal * (1 - descuento), 80_000_000)
        price_int = int(price)

        resumen = (
            f"Tu vivienda de {data.area}m² en la zona {data.location} de Cali "
            f"tiene un valor estimado de ${price_int:,.0f} COP "
            f"({round(price / 1_000_000, 1)} millones)."
        )

        return {
            "predicted_price": price_int,
            "confidence": 0.70,
            "model": "formula_colombia",
            "summary": resumen,
            "price_formatted": f"${price_int:,.0f} COP",
            "price_millions": round(price / 1_000_000, 1),
        }

    async def predict(self, data: HouseData) -> dict:
        if GROQ_API_KEY:
            try:
                return await self.predict_with_groq(data)
            except Exception as e:
                print(f"⚠️ Error con Groq, usando fórmula de respaldo: {e}")
                return self.fallback_prediction(data)

        return self.fallback_prediction(data)


predictor = HousePricePredictor()


@app.get("/")
async def read_root():
    return {
        "service": "HomeValue AI",
        "version": "3.1",
        "status": "running",
        "ia_activa": bool(GROQ_API_KEY),
        "model": "llama-3.1-8b-instant (Groq)" if GROQ_API_KEY else "formula_colombia",
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "ia_activa": bool(GROQ_API_KEY),
    }


@app.post("/predict")
async def predict_price(data: HouseData):
    try:
        print(
            f"\n📥 Solicitud: {data.area}m² | {data.rooms} hab | "
            f"{data.bathrooms} baños | {data.parking} parq | "
            f"{data.age} años | {data.location}"
        )

        result = await predictor.predict(data)

        # Compatibilidad con tu frontend actual:
        # el frontend espera predicted_price directamente en el JSON raíz
        return result

    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    print("=" * 55)
    print("  HomeValue AI — Predicción con IA v3.1")
    print("  Modelo: Llama 3.1 8B (Meta) vía Groq")
    print("=" * 55)
    print(f"  IA activa: {'✅ Sí' if GROQ_API_KEY else '❌ No'}")
    print("  Servidor:  http://localhost:8000")
    print("  Docs:      http://localhost:8000/docs")
    print("=" * 55)

    uvicorn.run(app, host="0.0.0.0", port=8000)