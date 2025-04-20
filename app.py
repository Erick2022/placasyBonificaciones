import tempfile
import pytesseract
from pdf2image import convert_from_path
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
from PIL import Image
import os
from flask import Flask, render_template, request, jsonify
import time
from config.config import ruta_pdf, ruta_guardado_imagenes
import logging
import requests
from io import BytesIO
from config  import main 
# Cargar variables desde .env
load_dotenv()

# Configurar Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

# Crear la instancia de Flask
app = Flask(__name__)

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No se encontró archivo'}), 400

    file_to_upload = request.files['file']

    if file_to_upload.filename == '':
        return jsonify({'error': 'Nombre de archivo vacío'}), 400

    try:
        result = cloudinary.uploader.upload(file_to_upload, resource_type="raw", folder="bonificaciones_pdfs")
        return jsonify({
            'message': 'PDF subido con éxito',
            'url': result['secure_url']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Crear directorios si no existen
os.makedirs(RUTA_PDF, exist_ok=True)
os.makedirs(RUTA_GUARDADO_IMAGENES, exist_ok=True)

# Configuración de logging
logging.basicConfig(level=logging.DEBUG)
logging.debug("Iniciando aplicación Flask...")

print(f"RUTA_PDF: {ruta_pdf}")
print(f"RUTA_GUARDADO_IMAGENES: {ruta_guardado_imagenes}")

# Palabras clave a buscar en las imágenes extraídas
palabras_clave = ["BONIFICACION", "AUTORIZACION", "RESOLUCION SUBDIRECTORAL"]

# Función para extraer texto de las imágenes usando OCR
def extraer_texto_de_imagen(imagen):
    texto = pytesseract.image_to_string(imagen)
    return texto

# Función para procesar los PDFs
def procesar_pdf(pdf_path):
    # Usar tempfile para guardar el PDF de manera temporal
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_file:
        with open(pdf_path, "rb") as file:
            tmp_file.write(file.read())  # Escribe el contenido del PDF en el archivo temporal
        temp_path = tmp_file.name  # Obtén la ruta temporal para el PDF

    # Convertir el PDF en imágenes
    imagenes = convert_from_path(temp_path)

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
    placas = request.json.get('placas', '')
    if not placas:
        return jsonify({"error": "No se proporcionaron placas"}), 400

    placas = [placa.strip() for placa in placas.split(',')]
    resultados = []

    # Listar archivos PDF en Cloudinary
    try:
        recursos = cloudinary.Search() \
            .expression("resource_type:raw AND folder:bonificaciones_pdfs") \
            .execute()
        
        for item in recursos.get('resources', []):
            file_name = item['filename']
            file_url = item['secure_url']

            if any(placa in file_name for placa in placas):
                print(f"📄 Descargando y procesando {file_name} desde Cloudinary")
                
                # Descargar el archivo PDF desde Cloudinary
                response = requests.get(file_url)
                if response.status_code == 200:
                    pdf_bytes = BytesIO(response.content)
                    # Guardar temporalmente como archivo
                    temp_path = tempfile.mktemp(suffix=".pdf")
                    with open(temp_path, 'wb') as f:
                        f.write(pdf_bytes.getbuffer())
                    resultados += procesar_pdf(temp_path)
                else:
                    print(f"❌ Error al descargar {file_name}: {response.status_code}")
    except Exception as e:
        return jsonify({"error": f"Error al listar PDFs de Cloudinary: {str(e)}"}), 500

    if resultados:
        return jsonify({"resultados": resultados})
    else:
        return jsonify({"error": "No se encontraron bonificaciones para las placas ingresadas."}), 200

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
  main()

