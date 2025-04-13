#!/usr/bin/env bash

# Actualizar paquetes e instalar herramientas adicionales necesarias
apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    libjpeg-dev \
    zlib1g-dev \
    tesseract-ocr \
    libtesseract-dev

# Actualizar pip antes de instalar dependencias
pip install --upgrade pip setuptools wheel
