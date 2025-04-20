import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

# Carga las variables del archivo .env
load_dotenv()

# Configura Cloudinary con tus credenciales
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

# Ruta local donde están tus PDFs
ruta_pdfs = os.getenv("RUTA_PDF")

# Sube todos los archivos PDF de la carpeta
for nombre_archivo in os.listdir(ruta_pdfs):
    if nombre_archivo.endswith(".pdf"):
        ruta_completa = os.path.join(ruta_pdfs, nombre_archivo)
        nombre_sin_extension = os.path.splitext(nombre_archivo)[0]	
        print(f"Subiendo {nombre_archivo}...")
        cloudinary.uploader.upload(
            ruta_completa,
            resource_type="raw",  # importante para PDFs
            folder="bonificaciones_pdfs",  # puedes cambiar el nombre si quieres
	    public_id=nombre_sin_extension  # Aquí se guarda como 'placa' sin .pdf
        )
        print(f"{nombre_archivo} subido correctamente.\n")
