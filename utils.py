import os
import platform
from fuzzywuzzy import process
from cloudinary.search import Search

def buscar_archivo_por_public_id(public_id):
    """
    Busca un archivo en Cloudinary por su Public ID.

    Args:
        public_id (str): El Public ID del archivo a buscar.

    Returns:
        dict: Los resultados de la búsqueda en Cloudinary.
    """
    try:
        recursos = Search().expression(
            f"resource_type:raw AND public_id={public_id}"
        ).execute()
        return recursos
    except Exception as e:
        raise Exception(f"Error al buscar el archivo en Cloudinary: {str(e)}")

def obtener_rutas():
    sistema_operativo = platform.system().lower()  # 'windows', 'linux', 'darwin'

    if sistema_operativo == "linux":
        ruta_pdf = os.getenv("ruta_pdf")
        ruta_guardado_imagenes = os.getenv("ruta_guardado_imagenes")
    elif sistema_operativo == "windows":
        ruta_pdf = os.getenv("RUTA_PDF_WINDOWS")
        ruta_guardado_imagenes = os.getenv("RUTA_GUARDADO_IMAGENES_WINDOWS")
    elif sistema_operativo == "darwin":  # Soporte para MacOS
        ruta_pdf = os.getenv("RUTA_PDF_MAC")
        ruta_guardado_imagenes = os.getenv("RUTA_GUARDADO_IMAGENES_MAC")
    else:
        raise ValueError(
            f"⚠️ Sistema operativo no compatible: {sistema_operativo}"
        )

    if not ruta_pdf or not ruta_guardado_imagenes:
        raise ValueError(
            "⚠️ Las rutas no están configuradas correctamente en el archivo .env"
        )

    return ruta_pdf, ruta_guardado_imagenes

def buscar_coincidencia_aproximada(placa_ingresada, todas_las_placas):
    """
    Busca una coincidencia aproximada para la placa ingresada en la lista de todas las placas.
    
    Args:
        placa_ingresada (str): La placa proporcionada por el usuario.
        todas_las_placas (list): Lista de todas las placas disponibles en Cloudinary.
    
    Returns:
        str: La placa más similar encontrada o None si no se encuentra ninguna coincidencia.
    """
    # Buscar la placa más similar a la ingresada
    coincidencia, puntaje = process.extractOne(placa_ingresada, todas_las_placas)

    # Definir un umbral de similitud (por ejemplo, 80%)
    if puntaje >= 80:  # Puedes ajustar el umbral según sea necesario
        return coincidencia
    return None
# Al final del archivo
print("utils.py cargado correctamente")  # Línea temporal
