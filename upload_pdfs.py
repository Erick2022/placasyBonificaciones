import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()

# Configurar Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

# Ruta local donde están tus PDFs nuevos
carpeta_local = os.getenv("RUTA_PDF", "/home/fedoraerick/Descargas/placas_BONIFICACIONES")

for archivo in os.listdir(carpeta_local):
    if archivo.endswith(".pdf"):
        ruta_completa = os.path.join(carpeta_local, archivo)
        response = cloudinary.uploader.upload(
            ruta_completa,
            resource_type="raw",
            folder="bonificaciones_pdfs"  # asegúrate que el código principal también lee desde esta carpeta
        )
        print(f"✅ Subido: {archivo} → {response['secure_url']}")
