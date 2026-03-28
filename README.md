🏠 HomeValue AI

Aplicación full-stack para estimar el precio de viviendas utilizando inteligencia artificial y arquitectura de microservicios desplegable en la nube.

⸻

🚀 Descripción

HomeValue AI es una plataforma que permite estimar el valor de una propiedad ingresando características como:
	•	Área (m²)
	•	Número de habitaciones
	•	Baños
	•	Parqueaderos
	•	Antigüedad
	•	Ubicación

El sistema utiliza un modelo de inteligencia artificial (LLM - Llama 3.1 vía Groq) para generar estimaciones basadas en razonamiento contextual del mercado.

Además, cada predicción se guarda en un historial persistente en base de datos.

⸻

🧱 Arquitectura

La aplicación está compuesta por tres microservicios:

🔹 Frontend
	•	Framework: React + Vite
	•	Puerto: 3000
	•	Función: interfaz de usuario

🔹 Prediction Service
	•	Framework: FastAPI
	•	Puerto: 8000
	•	Función: cálculo de precios usando IA (Groq + Llama 3.1)

🔹 History Service
	•	Framework: FastAPI
	•	Puerto: 8001
	•	Función: almacenamiento y consulta del historial

🔹 Base de Datos
	•	PostgreSQL
	•	Persistencia de predicciones

⸻

🐳 Dockerización

Cada servicio está dockerizado:
	•	homevalue-frontend
	•	homevalue-prediction
	•	homevalue-history
	•	postgres

⸻

🧪 Ejecución local (Docker Compose)
