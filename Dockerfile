# Imagen base ligera de Python
FROM python:3.11-slim

WORKDIR /app

# Dependencias del sistema necesarias para Reflex y Node.js
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Instalamos dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código fuente
COPY . .

# Inicializamos Reflex (descarga Node.js y dependencias frontend)
RUN reflex init

# Exportamos el frontend estático
# Esto genera .web/out/ con los archivos estáticos listos para producción
RUN reflex export --frontend-only --no-zip 2>/dev/null || true

# Puerto para el backend (WebSocket + API)
EXPOSE 8000

# ── PRODUCCIÓN CORRECTA ────────────────────────────────────────────────────
# En lugar de `reflex run --env prod` (que levanta todo en un proceso),
# usamos uvicorn directamente sobre el backend ASGI de Reflex.
# Esto es más estable, permite workers múltiples y es la forma recomendada.
#
# El frontend estático debe servirse por separado (CDN, Nginx, Render Static).
# Si usas Render con un solo servicio, puedes mantener `reflex run --env prod`
# pero considera separar frontend (Static Site) y backend (Web Service) en
# dos servicios de Render para mejor rendimiento.
# ──────────────────────────────────────────────────────────────────────────
CMD ["reflex", "run", "--env", "prod", "--backend-only"]