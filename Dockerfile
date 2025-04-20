# Usa una imagen base de Python
FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de tu proyecto dentro del contenedor
COPY . /app

# Instala las dependencias de tu proyecto
RUN pip install --upgrade pip && pip install -r requirements.txt

# Exponer el puerto en el que Flask corre
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000"]

