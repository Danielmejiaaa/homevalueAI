# 🏠 HomeValue AI
Aplicación full-stack para estimar el precio de viviendas en Cali, Colombia, utilizando inteligencia artificial y arquitectura de microservicios.

---

## 🚀 Descripción

HomeValue AI permite estimar el valor de mercado de una propiedad ingresando sus características:

- Área (m²)
- Número de habitaciones
- Baños
- Parqueaderos
- Antigüedad (años)
- Ubicación (norte, sur, centro, este, oeste)

El sistema utiliza **Llama 3.1 (Meta) vía Groq API** como motor de inteligencia artificial. El modelo recibe el contexto del mercado inmobiliario de Cali 2024-2025 y razona como un tasador experto para generar una estimación con rango de precios y justificación. Cada predicción queda registrada en un historial persistente.

---

## 🧱 Arquitectura

La aplicación está compuesta por tres microservicios independientes:

### 🔹 Frontend
- Framework: React + Vite
- Puerto local: `5173`
- Función: interfaz de usuario para ingresar datos y visualizar resultados

### 🔹 Prediction Service
- Framework: FastAPI (Python)
- Puerto local: `5000`
- Función: recibe los datos de la vivienda, consulta la IA (Llama 3.1 vía Groq) y retorna el precio estimado con justificación
- Fallback: fórmula de valoración calibrada para el mercado colombiano si la IA no está disponible

### 🔹 History Service
- Framework: FastAPI (Python)
- Puerto local: `5001`
- Función: almacena y consulta el historial de predicciones en PostgreSQL

### 🔹 Base de Datos
- Motor: PostgreSQL
- Función: persistencia del historial de predicciones

---

## 🤖 Modelo de IA

| Característica | Detalle |
|---|---|
| Modelo | `llama-3.1-8b-instant` (Meta) |
| Proveedor | Groq API (gratuito) |
| Tipo | LLM — Large Language Model |
| Enfoque | Razonamiento contextual con datos del mercado de Cali |
| Fallback | Fórmula de valoración por zona (norte/sur/centro/este/oeste) |

El modelo no fue entrenado específicamente con datos inmobiliarios colombianos. En su lugar, se le proporciona contexto de precios reales de Cali 2024-2025 en el prompt para que razone como un tasador experto.

---

## 🐳 Dockerización

Cada servicio tiene su propio `Dockerfile`. El proyecto incluye `docker-compose.yml` para levantar todos los servicios juntos:

```bash
docker-compose up --build
```

Servicios definidos:
- `homevalue-frontend`
- `homevalue-prediction`
- `homevalue-history`
- `postgres`

---

## 🧪 Ejecución local (sin Docker)

### Requisitos
- Python 3.11+
- Node.js 18+
- API Key de Groq (gratuita en [console.groq.com](https://console.groq.com))

### Prediction Service
```bash
cd prediction-service
pip install -r requirements.txt
$env:GROQ_API_KEY="tu_api_key"   # Windows PowerShell
python main.py
# Disponible en http://localhost:5000
# Docs en http://localhost:5000/docs
```

### History Service
```bash
cd history-service
pip install -r requirements.txt
python main.py
# Disponible en http://localhost:5001
```

### Frontend
```bash
cd frontend
npm install
npm run dev
# Disponible en http://localhost:5173
```

---

## 📡 API — Prediction Service

### `POST /predict`

**Body:**
```json
{
  "area": 120,
  "rooms": 3,
  "bathrooms": 2,
  "parking": 1,
  "age": 5,
  "location": "norte"
}
```

**Respuesta:**
```json
{
  "success": true,
  "data": {
    "predicted_price": 540000000,
    "price_min": 480000000,
    "price_max": 600000000,
    "price_formatted": "$540,000,000 COP",
    "price_millions": 540.0,
    "model": "llama-3.1-groq-ia",
    "summary": "Tu vivienda de 120m² en el norte de Cali tiene un valor estimado de $540 millones COP.",
    "key_factors": ["ubicación premium zona norte", "buen estado de conservación", "parqueadero incluido"]
  }
}
```

---

## ☁️ Despliegue en la nube

El proyecto está preparado para desplegarse en **AWS EKS (Kubernetes)**. Los manifests de Kubernetes para `Deployment`, `Service` y `LoadBalancer` están pendientes de configuración final.

Alternativamente puede desplegarse en **Railway** apuntando cada servicio a su subdirectorio correspondiente.

---

## 🔐 Variables de entorno

| Variable | Servicio | Descripción |
|---|---|---|
| `GROQ_API_KEY` | prediction-service | API key de Groq (gratis en console.groq.com) |
| `DATABASE_URL` | history-service | Cadena de conexión PostgreSQL |

---
