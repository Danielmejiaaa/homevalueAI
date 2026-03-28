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

El sistema usa **Llama 3.1 8B (Meta) vía Groq** como motor de IA. El modelo recibe contexto del mercado inmobiliario de Cali 2024-2025 y razona como un tasador experto para generar una estimación con rango de precios y justificación. Cada predicción queda registrada en un historial persistente en PostgreSQL.

---

## 🧱 Arquitectura

```
homevalueAI/
├── frontend/           # React + Vite
├── prediction-service/ # FastAPI — motor de IA
├── history-service/    # FastAPI — historial
├── docker-compose.yml
└── README.md
```

### 🔹 Frontend
- Framework: React + Vite
- Puerto: `3000`

### 🔹 Prediction Service
- Framework: FastAPI (Python)
- Puerto: `8000`
- Función: consulta Llama 3.1 vía Groq y retorna precio estimado con justificación
- Fallback: fórmula de valoración calibrada para el mercado colombiano

### 🔹 History Service
- Framework: FastAPI (Python)
- Puerto: `8001`
- Función: almacena y consulta el historial de predicciones

### 🔹 Base de Datos
- Motor: PostgreSQL

```sql
CREATE TABLE prediction_history (
    id SERIAL PRIMARY KEY,
    area REAL NOT NULL,
    rooms INTEGER NOT NULL,
    bathrooms INTEGER NOT NULL,
    parking INTEGER NOT NULL,
    age INTEGER NOT NULL,
    location VARCHAR(100) NOT NULL,
    predicted_price INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🤖 Modelo de IA

| Característica | Detalle |
|---|---|
| Modelo | `llama-3.1-8b-instant` (Meta) |
| Proveedor | Groq API |
| Tipo | LLM — Large Language Model |
| Enfoque | Razonamiento contextual con precios reales de Cali |
| Fallback | Fórmula de valoración por zona cuando la API no está disponible |

El modelo no fue entrenado específicamente con datos inmobiliarios colombianos. Se le proporciona contexto de precios reales de Cali en el prompt para que razone como un tasador experto.

---

## 🐳 Ejecución local (Docker Compose)

```bash
docker-compose up --build
```

### Accesos:
| Servicio | URL |
|---|---|
| Frontend | http://localhost:3000 |
| Prediction API | http://localhost:8000/docs |
| History API | http://localhost:8001/docs |

---

## 🔐 Variables de entorno

### Prediction Service
```env
GROQ_API_KEY=your_api_key_here
```

> Obtén tu API key gratuita en [console.groq.com](https://console.groq.com)

---

## 📡 API Endpoints

### Prediction Service

**`POST /predict`**
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

### History Service

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/records` | Lista el historial de predicciones |
| `POST` | `/records` | Guarda una nueva predicción |

---

## ☁️ Despliegue en AWS

Infraestructura definida:

| Servicio AWS | Uso |
|---|---|
| **ECR** | Almacenamiento de imágenes Docker ✅ |
| **EKS** | Clúster Kubernetes 🔄 En progreso |
| **IAM** | Gestión de permisos |
| **CloudFormation** | Provisión de recursos |

---

## ✅ Estado del proyecto

### Completado
- Microservicios funcionales (frontend, prediction, history)
- Integración frontend ↔ backend
- Persistencia en PostgreSQL
- Dockerización completa
- Docker Compose funcionando
- Push de imágenes a AWS ECR

### En progreso
- Despliegue en EKS
- Configuración de Kubernetes
- LoadBalancer público
- CI/CD

---

## ⚠️ Notas importantes

- La ubicación acepta únicamente: `norte`, `sur`, `centro`, `este`, `oeste`
- La API key de Groq es requerida para activar el modelo IA
- Sin API key el sistema usa la fórmula de valoración de respaldo

---
