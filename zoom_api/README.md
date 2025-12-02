# Zoom Data API

API REST desarrollada en Python/FastAPI para exponer datos de asistencia de Zoom desde archivos CSV. Diseñada para ser consumida por n8n.

## Requisitos Previos

- Python 3.8 o superior
- Acceso a la carpeta de archivos CSV de Zoom

## Instalación

1.  **Clonar o copiar** la carpeta del proyecto `zoom_api`.
2.  **Crear entorno virtual** (opcional pero recomendado):
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
3.  **Instalar dependencias**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configuración**:
    - Copiar `.env.example` a `.env`.
    - Editar `.env` con los valores correctos:
        - `API_KEY`: Definir una clave segura.
        - `CSV_FOLDER_PATH`: Ruta absoluta a la carpeta de CSVs (ej: `C:\Users\Kazzter\Desktop\Grupo Nods\Cesa Dashboards\zoom\csvs_diarios`).

## Ejecución

### Ejecución Manual
Doble click en el archivo `ejecutar_api.bat` o ejecutar en terminal:
```bash
python -m app.main
```

### Ejecución como Servicio de Windows (NSSM)
Para que la API se ejecute automáticamente al iniciar Windows y se reinicie en caso de error, use NSSM (Non-Sucking Service Manager).

1.  Descargar NSSM y copiar `nssm.exe` a una ruta del sistema (o dentro de la carpeta `scripts`).
2.  Abrir CMD como Administrador.
3.  Ejecutar:
    ```cmd
    nssm install ZoomDataAPI
    ```
4.  En la ventana de configuración:
    - **Path**: Ruta al ejecutable de python (ej: `C:\Users\...\zoom_api\venv\Scripts\python.exe` o el python global).
    - **Startup directory**: Ruta a la carpeta `zoom_api`.
    - **Arguments**: `-m app.main`
    - **Environment**: Agregar variables si es necesario, o confiar en el archivo `.env`.
5.  Click en "Install service".
6.  Iniciar el servicio: `nssm start ZoomDataAPI`

## Documentación de Endpoints

La documentación interactiva (Swagger UI) está disponible en `http://localhost:8000/docs`.

### Autenticación
Todos los endpoints requieren el header:
`X-API-Key: <TU_CLAVE_API>`

### Endpoints Principales

-   `GET /api/clases`: Lista todas las clases.
    -   Filtros: `fecha_inicio`, `fecha_fin`, `profesor`, `mes`.
    -   Paginación: `page`, `limit`.
-   `GET /api/clases/{id}`: Detalle de una clase.
-   `GET /api/estadisticas`: Resumen estadístico.
-   `GET /api/profesores`: Lista de profesores.
-   `GET /api/health`: Estado del sistema.

## Integración con n8n

### Nodo HTTP Request
Configurar el nodo HTTP Request en n8n de la siguiente manera:

-   **Method**: GET
-   **URL**: `http://localhost:8000/api/clases` (o la IP del servidor Windows)
-   **Authentication**: Generic Credential Type -> Header Auth
-   **Header Auth**:
    -   Name: `X-API-Key`
    -   Value: `<TU_CLAVE_API>`
-   **Query Parameters**: Agregar según necesidad (ej: `mes` = `{{ $now.format('MM') }}`).

### Ejemplo de Respuesta JSON
```json
{
  "success": true,
  "data": [
    {
      "Meeting ID": 123456,
      "Topic": "Clase 1",
      ...
    }
  ],
  "meta": {
    "total": 50,
    "page": 1,
    "limit": 50
  }
}
```
