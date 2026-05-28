# Usamos una imagen ligera de Python
FROM python:3.11-slim

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalamos utilidades necesarias para que Reflex empaquete el frontend
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Copiamos las dependencias y las instalamos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto de tu código al contenedor
COPY . .

# Compilamos el frontend durante la construcción
RUN reflex export --frontend-only

# Exponemos el puerto estándar
EXPOSE 8000

# Iniciamos la app en modo producción
CMD ["reflex", "run", "--env", "prod"]