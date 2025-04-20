
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
credenciales_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

try:
    creds = service_account.Credentials.from_service_account_file(credenciales_path)
    service = build('drive', 'v3', credentials=creds)
    
    # Probar acceso listando los primeros archivos en Drive
    results = service.files().list(pageSize=5).execute()
    files = results.get('files', [])
    
    if not files:
        print("No se encontraron archivos en Google Drive.")
    else:
        print("Archivos encontrados en Google Drive:")
        for file in files:
            print(f"{file['name']} ({file['id']})")

except Exception as e:
    print(f"Error en la autenticación: {e}")
