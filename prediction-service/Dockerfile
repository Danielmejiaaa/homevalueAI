FROM python:3.12-slim

WORKDIR /app

# Evitar archivos pyc y mejorar logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copiar archivo de dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Exponer el puerto del servicio
EXPOSE 8000

# Comando para iniciar la API
CMD ["python", "main.py"]