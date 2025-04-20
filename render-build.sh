#!/usr/bin/env bash

# Actualizar paquetes e instalar herramientas adicionales necesarias en Fedora
dnf update -y && dnf install -y \
    gcc \
    gcc-c++ \
    make \
    glib2-devel \
    dbus-devel \
    libffi-devel \
    openssl-devel \
    libxml2-devel \
    libxslt-devel \
    zlib-devel \
    cairo-devel \
    pkg-config \
    meson \
    ninja-build \
    python3-devel \
    python3-pip \
    libjpeg-turbo-devel \
    tesseract-devel \
    tesseract-langpack-eng

# Actualizar pip antes de instalar dependencias
pip install --upgrade pip setuptools wheel
