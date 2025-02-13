import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os
from flask import Flask, render_template, request, jsonify
import time
from config.config import ruta_pdf, ruta_guardado_imagenes, credentials
import logging
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Crear directorios si no existen
os.makedirs(ruta_pdf, exist_ok=True)
os.makedirs(ruta_guardado_imagenes, exist_ok=True)

# Configuración de logging
logging.basicConfig(level=logging.DEBUG)
logging.debug("Iniciando aplicación Flask...")

print(f"RUTA_PDF: {ruta_pdf}")
print(f"RUTA_GUARDADO_IMAGENES: {ruta_guardado_imagenes}")

# Crear la instancia de Flask
app = Flask(__name__)

# Palabras clave a buscar en las imágenes extraídas
palabras_clave = ["BONIFICACION", "AUTORIZACION", "RESOLUCION SUBDIRECTORAL"]

# Función para extraer texto de las imágenes usando OCR
def extraer_texto_de_imagen(imagen):
    texto = pytesseract.image_to_string(imagen)
    return texto

# Función para procesar los PDFs
def procesar_pdf(pdf_path):
    # Convertir el PDF en imágenes
    imagenes = convert_from_path(pdf_path)

    resultados = []

    for i, imagen in enumerate(imagenes):
        # Extraer texto de la imagen
        texto_extraido = extraer_texto_de_imagen(imagen)
        
        # Verificar si alguna palabra clave está en el texto extraído
        if any(palabra in texto_extraido.upper() for palabra in palabras_clave):
            print(f"Bonificación encontrada en {pdf_path}, página {i + 1}")
            # Guardar la imagen si contiene la palabra clave
            imagen_guardada = f"{os.path.basename(pdf_path)}_page_{i + 1}.jpg"
            imagen_guardada_path = os.path.join(ruta_guardado_imagenes, imagen_guardada)
            imagen.save(imagen_guardada_path, "JPEG")
            resultados.append(f"Bonificación encontrada en {pdf_path}, página {i + 1}")
            print(f"Imagen guardada en {imagen_guardada_path}")
        else:
            print(f"No se encontró bonificación en {pdf_path}, página {i + 1}")

    return resultados

# Ruta para mostrar el formulario
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para procesar las placas
@app.route('/procesar_placas', methods=['POST'])
def procesar_placas():
    # Obtener las placas enviadas desde el frontend
    placas = request.json.get('placas', '').split(',')
    if not placas:
        return jsonify({"error": "No se proporcionaron placas"}), 400

    # Limpiar las placas (eliminar espacios adicionales)
    placas = [placa.strip() for placa in placas]

    # Procesar las placas
    resultados = []
    # Filtrar los archivos PDF que contienen alguna de las placas ingresadas
    archivos_pdf = [f for f in os.listdir(ruta_pdf) if f.endswith('.pdf') and any(placa in f for placa in placas)]
    # Procesar los archivos PDF que coinciden con las placas
    for archivo_pdf in archivos_pdf:
        pdf_path = os.path.join(ruta_pdf, archivo_pdf)
        resultados += procesar_pdf(pdf_path)
    # Devolver los resultados al frontend
    if resultados:
        return jsonify({"resultados": resultados})
    else:
        return jsonify({"error": "No se encontraron bonificaciones para las placas ingresadas."}), 200
    
@app.route('/listar_archivos_drive', methods=['GET'])
def listar_archivos_drive():
    try:
        # Crear el servicio de Google Drive con las credenciales cargadas desde config.py
        service = build('drive', 'v3', credentials=credentials)

        # Listar los archivos en Google Drive
        results = service.files().list(pageSize=10, fields="files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            return jsonify({'message': 'No files found on Google Drive.'})
        else:
            files = [{'name': item['name'], 'id': item['id']} for item in items]
            return jsonify({'files': files})

    except HttpError as error:
        return jsonify({'error': f'An error occurred: {error}'})
        
@app.route('/process', methods=['GET'])
def process():
    # Simular un proceso largo (por ejemplo, 20 segundos)
    time.sleep(10)
    
    # Respuesta simulada
    data = {
        "message": "Proceso completado",
        "images": [
            "imagen1.jpg",
            "imagen2.jpg",
            "imagen3.jpg"
        ]
    }   
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
