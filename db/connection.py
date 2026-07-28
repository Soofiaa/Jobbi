import os
import sys
from supabase import create_client, Client
from dotenv import load_dotenv

def _ruta_base():
    """Retorna la ruta base correcta tanto en desarrollo como en .exe"""
    if getattr(sys, 'frozen', False):
        # Ejecutando como .exe compilado por PyInstaller
        return os.path.dirname(sys.executable)
    else:
        # Ejecutando como script Python normal
        # Fix: apuntaba a db/ (carpeta de este archivo) en vez de a la raíz del proyecto,
        # donde vive el .env.
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_env_path = os.path.join(_ruta_base(), ".env")
load_dotenv(dotenv_path=_env_path)

_client: Client = None

def get_client() -> Client:
    global _client
    if _client is None:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        if not url or not key:
            raise ValueError("Faltan las credenciales de Supabase en el archivo .env")
        _client = create_client(url, key)
    return _client