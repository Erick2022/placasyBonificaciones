#!/usr/bin/env bash
set -o errexit  # Detiene la ejecución si hay errores

echo "Instalando dependencias de Python..."
pip install --no-cache-dir -r requirements.txt

