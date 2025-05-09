# 📊 Serapis Metrics Library

Una biblioteca simple y eficiente para recopilar métricas de uso en proyectos Serapis, compatible con Python 2.7, Python 3.x y PyRevit.

## 🚀 Características

- Seguimiento de métricas de uso
- Identificación única de usuarios
- Manejo automático de errores
- Fácil integración con cualquier proyecto Python
- Compatibilidad con Python 2.7, Python 3.x y PyRevit

## 📋 Requisitos

- Python 2.7 o superior
- Conexión a internet para enviar métricas
- Para PyRevit: IronPython 2.7

## 💻 Instalación

### Usando pip

```bash
pip install serapis-metrics
```

### Desde el código fuente

```bash
git clone https://github.com/asmorodina/serapis-metrics.git
cd serapis-metrics
pip install -e .
```

## 🔧 Configuración

La biblioteca usa variables de entorno para su configuración:

```bash
# URL del backend (opcional, valor por defecto: http://localhost:3000)
export SERAPIS_BACKEND_URL="http://tu-backend.com"
```

## 📖 Uso

### Ejemplo Básico (Python 3.x)

```python
from serapis_metrics import initialize_metrics

# Tu ID de versión
version_id = "tu-version-id"

# Inicializar métricas
initialize_metrics(version_id)
print("Métricas inicializadas correctamente")
```

### Ejemplo con PyRevit

```python
# En tu script de PyRevit
from serapis_metrics import initialize_metrics, track_usage

# Tu ID de versión
version_id = "tu-version-id"

# Inicializar métricas
try:
    initialize_metrics(version_id)
    print("Métricas inicializadas correctamente")
except Exception as e:
    print("Error al inicializar métricas: {}".format(e))
```

### Seguimiento Personalizado de Uso

```python
from serapis_metrics import track_usage, get_user_hash

# Obtener el hash del usuario
user_hash = get_user_hash()

# Registrar uso específico
track_usage(user_hash, "tu-version-id")
```

### Manejo de Errores

```python
from serapis_metrics import report_error

try:
    # Tu código aquí
    resultado = alguna_funcion()
except Exception as e:
    # Reportar el error
    report_error(e, context="nombre_de_la_funcion")
```

## 📚 Referencia de API

### `initialize_metrics(version_id: str)`

Inicializa el sistema de métricas para una versión específica.

- **Parámetros:**
  - `version_id` (str): Identificador único de versión

- **Excepciones:**
  - Lanza una excepción si hay problemas de conexión o inicialización

### `track_usage(user_hash: str, version_id: str)`

Registra el uso de una versión específica por un usuario.

- **Parámetros:**
  - `user_hash` (str): Hash único del usuario
  - `version_id` (str): Identificador de versión

- **Excepciones:**
  - RuntimeError: Si hay problemas al enviar las métricas

### `get_user_hash() -> str`

Obtiene o genera un hash único para el usuario actual.

- **Retorna:**
  - str: Hash único del usuario

- **Excepciones:**
  - Lanza una excepción si no se puede generar o recuperar el hash

### `report_error(exception_obj: Exception, context: str = None)`

Envía información de error al backend.

- **Parámetros:**
  - `exception_obj` (Exception): El error que ha sido capturado
  - `context` (str, opcional): Nombre de la función o parte del código donde ocurrió el error

## 🔍 Notas de Compatibilidad

### Python 2.7
- Compatible con IronPython 2.7 (PyRevit)
- Usa `urllib2` para peticiones HTTP
- Soporta variables de entorno del sistema

### Python 3.x
- Usa `urllib.request` para peticiones HTTP
- Soporta todas las características modernas de Python
- Manejo mejorado de strings Unicode

### PyRevit
- Compatible con el entorno de IronPython 2.7
- Usa `System.Environment` para variables de entorno
- Optimizado para el entorno de Revit

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor, lee [CONTRIBUTING.md](CONTRIBUTING.md) para detalles sobre nuestro código de conducta y el proceso para enviarnos pull requests.

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE.md](LICENSE.md) para más detalles.