import os
import json
import io
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# Cargar las variables de entorno
load_dotenv()

# Validar y cargar GOOGLE_CREDENTIALS_JSON
google_credentials_path = os.getenv('GOOGLE_CREDENTIALS_JSON_PATH')

if not google_credentials_path:
    raise ValueError("⚠️ GOOGLE_CREDENTIALS_JSON_PATH no está definido en el entorno.")

if not os.path.exists(google_credentials_path):
    raise FileNotFoundError(f"⚠️ No se encontró el archivo de credenciales en {google_credentials_path}")

try:
    with open(google_credentials_path, "r") as f:
        credentials_info = json.load(f)
    
    credentials = service_account.Credentials.from_service_account_info(credentials_info)
    print("✅ Credenciales cargadas correctamente.")
except json.JSONDecodeError as e:
    raise ValueError(f"❌ Error al decodificar GOOGLE_CREDENTIALS_JSON_PATH: {e}")
except Exception as e:
    raise RuntimeError(f"❌ Error inesperado al cargar credenciales: {e}")

# Obtener rutas desde el entorno o usar valores predeterminados
ruta_pdf = os.getenv("RUTA_PDF", "/home/fedoraerick/Descargas/placas_BONIFICACIONES")
ruta_guardado_imagenes = os.getenv("RUTA_GUARDADO_IMAGENES", "/home/fedoraerick/Documentos/bonificaciones_extraidas")

print(f"📂 Ruta PDF: {ruta_pdf}")
print(f"📂 Ruta de guardado de imágenes: {ruta_guardado_imagenes}")

# Crear las carpetas si no existen
for ruta in [ruta_pdf, ruta_guardado_imagenes]:
    os.makedirs(ruta, exist_ok=True)

# Definir los alcances necesarios para Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
credentials = credentials.with_scopes(SCOPES)

# Autenticar y crear el servicio de Google Drive
service = build('drive', 'v3', credentials=credentials)

# ID de la carpeta en Google Drive
FOLDER_ID = "10iA3Md5lnMh1FwMsAf50OaFD9A4KnQv_"

def listar_archivos_en_drive(folder_id):
    """Lista los archivos dentro de una carpeta en Google Drive."""
    try:
        query = f"'{folder_id}' in parents and trashed=false"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        return results.get('files', [])
    except Exception as e:
        print(f"❌ Error al listar archivos en Google Drive: {e}")
        return []

def descargar_archivo(file_id, file_name, destino):
    """Descarga un archivo de Google Drive solo si no existe en el destino."""
    file_path = os.path.join(destino, file_name)
    
    if os.path.exists(file_path):
        print(f"📂 El archivo {file_name} ya existe. Omitiendo descarga.")
        return
    
    try:
        request = service.files().get_media(fileId=file_id)
        
        with open(file_path, "wb") as f:
            downloader = MediaIoBaseDownload(f, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(f"⬇️ Descargando {file_name}... {int(status.progress() * 100)}%")
        
        print(f"✅ Descarga completa: {file_path}")
    except Exception as e:
        print(f"❌ Error al descargar {file_name}: {e}")

# Listar archivos en la carpeta de Drive
archivos = listar_archivos_en_drive(FOLDER_ID)

# Descargar cada archivo en la carpeta local
for archivo in archivos:
    print(f"📥 Descargando: {archivo['name']}")
    descargar_archivo(archivo['id'], archivo['name'], ruta_pdf)
