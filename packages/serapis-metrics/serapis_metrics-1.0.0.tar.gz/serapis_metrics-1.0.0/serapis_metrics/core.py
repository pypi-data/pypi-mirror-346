from __future__ import print_function
import uuid
import os
import sys
import json
import time

# Compatibilidad con Python 2 y 3
try:
    # Python 3
    from urllib.request import Request, urlopen
    from urllib.error import URLError
    from System import Environment
except ImportError:
    # Python 2
    from urllib2 import Request, urlopen, URLError
    try:
        from System import Environment
    except ImportError:
        Environment = None

# Configuración
def get_env_var(name, default=None):
    """Obtiene variables de entorno de forma compatible con Python 2 y 3"""
    if Environment:
        return Environment.GetEnvironmentVariable(name) or default
    return os.environ.get(name, default)

backend_url = get_env_var("SERAPIS_BACKEND_URL", "http://localhost:3000")
url_register_hash = "{}/api/metrics/register-user-hash".format(backend_url)
url_metrics = "{}/api/metrics/register".format(backend_url)
error_url = "{}/api/metrics/client-error".format(backend_url)

headers = {
    "Origin": "http://localhost:4200",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def report_error(exception_obj, context=None):
    """
    Envía la información del error al backend.

    Args:
        exception_obj (Exception): El error que ha sido capturado.
        context (str, optional): El nombre de la función o parte del código donde ocurrió el error.
    """
    error_payload = {
        "function": context or "unknown",
        "error_message": str(exception_obj)
    }

    try:
        req = Request(
            error_url,
            data=json.dumps(error_payload).encode('utf-8'),
            headers=headers
        )
        urlopen(req, timeout=30)
    except Exception as req_err:
        print("[ERROR] No se pudo enviar el error al backend: {}".format(req_err))

def log_error(exc_type, exc_value, exc_traceback):
    """Registra excepciones no manejadas."""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    print("[ERROR] Excepción no manejada: {}".format(exc_value))

def get_user_hash():
    """Obtiene o crea un hash de usuario único."""
    file_path = os.path.join(os.path.expanduser("~"), ".serapis_user_id")

    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return f.read().strip()
        else:
            return create_new_user_hash(file_path)
    except Exception as e:
        print("[ERROR] No se pudo generar o leer el user_hash: {}".format(e))
        report_error(e, context="get_user_hash")
        raise

def create_new_user_hash(file_path):
    """Crea un nuevo hash de usuario y lo registra en el backend."""
    print("Iniciando generación del user_hash.")
    user_hash = str(uuid.uuid4())
    
    with open(file_path, 'w') as f:
        f.write(user_hash)

    system_user = get_env_var("USERNAME") or "unknown_user"
    timestamp = str(int(time.time()))

    payload = {
        "user_hash": user_hash,
        "systemUser": system_user,
        "versionId": version_id
    }

    try:
        req = Request(
            url_register_hash,
            data=json.dumps(payload).encode('utf-8'),
            headers=headers
        )
        response = urlopen(req, timeout=30)
        print("Response status: {}".format(response.getcode()))
        print("Response body: {}".format(response.read().decode('utf-8')))

        if response.getcode() not in [200, 201]:
            raise Exception("Error registrando user_hash: {} - {}".format(
                response.getcode(), response.read().decode('utf-8')))

        return user_hash
    except Exception as e:
        print("[ERROR] No se pudo registrar el user_hash: {}".format(e))
        report_error(e, context="create_new_user_hash")
        raise

def track_usage(user_hash, version_id):
    """Registra el uso de una versión específica."""
    payload = {
        'user_hash': user_hash,
        'versionId': version_id,
        'status': 'success',
    }

    try:
        req = Request(
            url_metrics,
            data=json.dumps(payload).encode('utf-8'),
            headers=headers
        )
        response = urlopen(req, timeout=30)
        print("Response status: {}".format(response.getcode()))
        print("Response body: {}".format(response.read().decode('utf-8')))

        if response.getcode() not in [200, 201]:
            raise Exception("El backend respondió con un error. {}: {}".format(
                response.getcode(), response.read().decode('utf-8')))
    except Exception as e:
        print("[ERROR] Error enviando métricas de uso: {}".format(e))
        report_error(e, context="track_usage")
        raise RuntimeError("Error enviando métricas: {}".format(e))

def initialize_metrics(version_id):
    """Inicializa el sistema de métricas."""
    try:
        user_hash = get_user_hash()
        track_usage(user_hash, version_id)
        print("Métricas enviadas exitosamente.")
    except Exception as e:
        print("[ERROR] No se pudo inicializar el sistema de métricas: {}".format(e))
        report_error(e, context="initialize_metrics")