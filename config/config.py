import os
import cloudinary
import cloudinary.api
import cloudinary.search
from dotenv import load_dotenv
import platform  # Detectar el sistema operativo
import requests

# Cargar variables de entorno
load_dotenv()

# Configurar Cloudinary
try:
    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET")
    )

    # Verificar que los valores de Cloudinary estén configurados
    if not all([cloudinary.config().cloud_name, cloudinary.config().api_key, cloudinary.config().api_secret]):
        raise ValueError("⚠️ Las credenciales de Cloudinary no están configuradas correctamente en el archivo .env")
except Exception as e:
    raise RuntimeError(f"Error al configurar Cloudinary: {e}")

# Detectar el sistema operativo
def obtener_rutas():
    sistema_operativo = platform.system().lower()  # 'windows', 'linux', 'darwin'

    if sistema_operativo == "linux":
        ruta_pdf = os.getenv("RUTA_PDF_LINUX")
        ruta_guardado_imagenes = os.getenv("RUTA_GUARDADO_IMAGENES_LINUX")
    elif sistema_operativo == "windows":
        ruta_pdf = os.getenv("RUTA_PDF_WINDOWS")
        ruta_guardado_imagenes = os.getenv("RUTA_GUARDADO_IMAGENES_WINDOWS")
    else:
        raise ValueError(f"⚠️ Sistema operativo no compatible: {sistema_operativo}")

    # Validar que las rutas estén definidas
    if not ruta_pdf or not ruta_guardado_imagenes:
        raise ValueError("⚠️ Las rutas no están configuradas correctamente en el archivo .env")

    return ruta_pdf, ruta_guardado_imagenes

# Crear directorios si no existen
def crear_directorios(ruta_pdf, ruta_guardado_imagenes):
    try:
        os.makedirs(ruta_pdf, exist_ok=True)
        os.makedirs(ruta_guardado_imagenes, exist_ok=True)
    except Exception as e:
        raise RuntimeError(f"⚠️ Error al crear los directorios: {e}")

# Función para descargar archivo desde Cloudinary
def descargar_archivo(public_id, nombre_archivo, ruta_destino):
    try:
        url = f"https://res.cloudinary.com/{cloudinary.config().cloud_name}/raw/upload/{public_id}.pdf"
        response = requests.get(url)
        if response.status_code == 200:
            with open(os.path.join(ruta_destino, nombre_archivo), 'wb') as f:
                f.write(response.content)
            print(f"✅ Archivo {nombre_archivo} descargado exitosamente.")
        else:
            print(f"❌ Error {response.status_code} al descargar {nombre_archivo}: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al descargar el archivo {nombre_archivo}: {e}")
    except Exception as e:
        print(f"❌ Error inesperado al descargar el archivo {nombre_archivo}: {e}")

# Buscar y descargar archivos desde Cloudinary
def buscar_y_descargar_archivos(ruta_pdf):
    try:
        recursos = cloudinary.search.Search() \
            .expression("resource_type:raw AND folder:bonificaciones_pdfs") \
            .execute()

        if 'resources' in recursos:
            for archivo in recursos['resources']:
                archivo_id = archivo['public_id']  # ID completo, incluyendo la carpeta
                archivo_nombre = archivo['filename'] + '.pdf'
                print(f"📥 Descargando: {archivo_nombre}")
                descargar_archivo(archivo_id, archivo_nombre, ruta_pdf)
        else:
            print("⚠️ No se encontraron archivos en Cloudinary.")
    except cloudinary.exceptions.Error as e:
        print(f"❌ Error al intentar buscar los archivos: {e}")
    except Exception as e:
        print(f"❌ Error inesperado durante la búsqueda y descarga: {e}")

# Flujo principal
def main():
    try:
        ruta_pdf, ruta_guardado_imagenes = obtener_rutas()
        crear_directorios(ruta_pdf, ruta_guardado_imagenes)
        print(f"📂 Ruta PDF: {ruta_pdf}")
        print(f"📂 Ruta de guardado de imágenes: {ruta_guardado_imagenes}")
        buscar_y_descargar_archivos(ruta_pdf)
    except Exception as e:
        print(f"❌ Error en la ejecución principal: {e}")

# Ejecutar el flujo principal
if __name__ == "__main__":
    main()
