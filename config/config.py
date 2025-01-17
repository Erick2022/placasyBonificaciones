import os
from google.oauth2 import service_account
import json
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Validar y cargar GOOGLE_CREDENTIALS_JSON
google_credentials = os.getenv('GOOGLE_CREDENTIALS_JSON')
if not google_credentials:
    raise ValueError("La variable GOOGLE_CREDENTIALS_JSON no está definida en el archivo .env.")

try:
    credentials_info = json.loads(google_credentials)
    print("Credenciales cargadas correctamente.")
except json.JSONDecodeError as e:
    raise ValueError(f"Error al decodificar GOOGLE_CREDENTIALS_JSON: {e}")

# Definir las rutas usando las variables de entorno
ruta_pdf = os.getenv("RUTA_PDF", "/home/fedoraerick/Descargas/placasBONIFICACIONESBACKUS")
ruta_guardado_imagenes = os.getenv("RUTA_GUARDADO_IMAGENES", "/home/fedoraerick/Documentos/bonificaciones_extraidas")

# Crear las carpetas si no existen
for ruta in [ruta_pdf, ruta_guardado_imagenes]:
    if not os.path.exists(ruta):
        os.makedirs(ruta)
        print(f"Directorio creado: {ruta}")
    else:
        print(f"El directorio ya existe: {ruta}")

# Crear las credenciales a partir del contenido JSON    
try:
    credentials = service_account.Credentials.from_service_account_info(credentials_info)
except Exception as e:
    raise ValueError(f"Error al crear las credenciales de servicio: {e}")

# Define los alcances necesarios para tu aplicación
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']  # Asegúrate de que el alcance es correcto
credentials = credentials.with_scopes(SCOPES)