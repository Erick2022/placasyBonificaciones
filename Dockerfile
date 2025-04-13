# Usar una imagen base oficial de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /opt/render/project

# Copiar los archivos de la aplicación al contenedor
COPY . .

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    libglib2.0-dev \
    libpoppler-cpp-dev \
    tesseract-ocr \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python listadas en requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Crear las carpetas necesarias para las rutas definidas en las variables de entorno
RUN mkdir -p /opt/render/project/files/pdf /opt/render/project/files/imagenes

# Exponer el puerto en el que correrá la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación en producción con Gunicorn 
CMD ["sh", "-c", "gunicorn -b 0.0.0.0:${PORT:-8000} app:app"]
