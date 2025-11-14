# Usamos una imagen ligera de Python
FROM python:3.10-slim

# Evita que Python genere archivos .pyc y buffer de salida
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalamos dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    gcc \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiamos el archivo ligero del servidor
COPY requirements-server.txt .

# Instalamos usando ese archivo
RUN pip install --no-cache-dir -r requirements-server.txt

# Copiamos todo el código del proyecto
COPY . .

# Exponemos el puerto 8000
EXPOSE 8000

# Comando para iniciar el servidor (escuchando en todas las interfaces 0.0.0.0)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
