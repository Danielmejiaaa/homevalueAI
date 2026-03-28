# HomeValue AI

Aplicación full-stack para estimar el precio de viviendas en Cali, Colombia, utilizando inteligencia artificial y una arquitectura de microservicios desplegada en AWS con Kubernetes.

---

## Descripción

HomeValue AI permite a los usuarios ingresar características de una vivienda (área, habitaciones, baños, etc.) y obtener una estimación de su precio mediante un modelo de predicción.

La aplicación está construida bajo una arquitectura de microservicios, donde cada componente cumple una función específica y se comunica mediante APIs REST. Además, cada predicción realizada se almacena en una base de datos para construir un historial consultable.

---

## Arquitectura del sistema

La aplicación está compuesta por los siguientes componentes:

- Frontend (React)
- Prediction Service (FastAPI)
- History Service (FastAPI)
- Base de datos PostgreSQL
- Kubernetes (EKS)
- Amazon ECR (registro de imágenes)

### Flujo de funcionamiento

1. El usuario accede al frontend.
2. El frontend envía una solicitud al prediction-service para obtener el precio estimado.
3. El prediction-service calcula el valor y responde.
4. El frontend envía los datos al history-service.
5. El history-service guarda la información en PostgreSQL.
6. El frontend consulta el historial y lo muestra al usuario.

---

## Estructura del proyecto

- **frontend/**  
  Aplicación React (UI)  
  - `src/` – Código fuente  
  - `Dockerfile` – Imagen del frontend  

- **prediction-service/**  
  Microservicio de predicción (FastAPI)  
  - `main.py` – Lógica principal / endpoints  
  - `Dockerfile`  

- **history-service/**  
  Microservicio de historial (FastAPI)  
  - `main.py` – Manejo de persistencia  
  - `Dockerfile`  

- **k8s/**  
  Manifiestos de Kubernetes  
  - `frontend-deployment.yaml`  
  - `prediction-deployment.yaml`  
  - `history-deployment.yaml`  
  - `postgres-deployment.yaml`  

- `docker-compose.yml` – Orquestación local  
- `README.md` – Documentación del proyecto



---

## Ejecución local

### Requisitos

- Docker
- Docker Compose

### Pasos

1. Clonar el repositorio:

```bash
git clone https://github.com/tu-usuario/homevalueAI
cd homevalueAI
```
## Ejecutar los servicios:
docker-compose up --build
## Acceder a la aplicación:
### Frontend: http://localhost:3000
### Prediction API: http://localhost:8000
### History API: http://localhost:8001

## Despliegue en AWS (EKS)
1. Construcción de imágenes
docker build -t homevalue-frontend ./frontend
docker build -t homevalue-prediction ./prediction-service
docker build -t homevalue-history ./history-service
2. Subida a Amazon ECR
docker tag <image> <aws_account>.dkr.ecr.us-east-1.amazonaws.com/<repo>
docker push <aws_account>.dkr.ecr.us-east-1.amazonaws.com/<repo>
3. Creación del clúster
eksctl create cluster --name homevalue-cluster
4. Despliegue en Kubernetes
kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f k8s/prediction-deployment.yaml
kubectl apply -f k8s/history-deployment.yaml
kubectl apply -f k8s/frontend-deployment.yaml
5. Exposición del frontend
El frontend se expone mediante un servicio tipo LoadBalancer, lo que genera una URL pública accesible desde internet.
## Base de datos
Se utiliza PostgreSQL desplegado dentro del clúster.
Tabla principal
CREATE TABLE prediction_history (
    id SERIAL PRIMARY KEY,
    area REAL,
    rooms INTEGER,
    bathrooms INTEGER,
    parking INTEGER,
    age INTEGER,
    location VARCHAR(100),
    predicted_price INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

## Variables de entorno
Ejemplo en history-service:
env:
  - name: DB_HOST
    value: "postgres"
  - name: DB_NAME
    value: "homevalue_db"
  - name: DB_USER
    value: "postgres"
  - name: DB_PASSWORD
    value: "postgres123"
  - name: DB_PORT
    value: "5432"

## Tecnologías utilizadas
### Frontend
1. React
2. JavaScript
3. CSS
### Backend
1. Python
2. FastAPI
### Base de datos
1. PostgreSQL
### Contenedores
1. Docker
2. Docker Compose
### Orquestación
1. Kubernetes (Amazon EKS)
### Cloud
1. AWS ECR (Elastic Container Registry)
2. AWS EKS (Elastic Kubernetes Service)

## Funcionalidades
1. Predicción de precios de vivienda
2. Validación de datos en frontend
3. Persistencia de datos en base de datos
4. Visualización de historial
5. Arquitectura de microservicios
6. Despliegue en Kubernetes

## Resultados
La aplicación permite:
1. Acceder desde internet mediante LoadBalancer
2. Realizar predicciones en tiempo real
3. Guardar y consultar historial persistente
4. Ejecutar todos los servicios dentro de Kubernetes

## Consideraciones
1. Los servicios backend se comunican mediante servicios internos de Kubernetes
2. La base de datos se encuentra dentro del clúster
3. Las imágenes se almacenan en Amazon ECR
4. El frontend consume APIs públicas desplegadas en AWS

## Posibles mejoras
1. Uso de Kubernetes Secrets para credenciales
2. Implementación de Ingress Controller
3. Uso de dominio personalizado
4. Autenticación de usuarios
5. Escalamiento automático (HPA)
