# Etapa 1: construir la aplicación con Node
FROM node:20-alpine AS builder

WORKDIR /app

# Copiar archivos de dependencias
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar el resto del proyecto
COPY . .

# Construir la app para producción
RUN npm run build

# Etapa 2: servir la app con Nginx
FROM nginx:alpine

# Copiar los archivos construidos a la carpeta pública de Nginx
COPY --from=builder /app/dist /usr/share/nginx/html

# Exponer el puerto 80
EXPOSE 80

# Comando por defecto de Nginx
CMD ["nginx", "-g", "daemon off;"]