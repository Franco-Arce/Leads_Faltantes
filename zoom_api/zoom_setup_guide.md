# Guía de Configuración: Zoom Server-to-Server OAuth para n8n

Para conectar n8n directamente a Zoom sin usar Python ni tu PC, necesitas crear una "Server-to-Server OAuth App". Esto te dará las credenciales para que n8n actúe como Administrador.

## Paso 1: Crear la App en Zoom
1.  Ve al [Zoom App Marketplace](https://marketplace.zoom.us/) e inicia sesión con tu cuenta de **Administrador**.
2.  Haz clic en **Develop** (arriba a la derecha) -> **Build App**.
3.  Busca **Server-to-Server OAuth** y haz clic en **Create**.
4.  Ponle un nombre, ej: `n8n Automation`.

## Paso 2: Obtener Credenciales
En la pantalla "App Credentials", verás 3 datos importantes. Cópialos, los necesitarás en n8n:
-   **Account ID**
-   **Client ID**
-   **Client Secret**

## Paso 3: Configurar Scopes (Permisos)
Ve a la pestaña **Scopes** y agrega los siguientes permisos para poder leer los reportes de asistencia:

-   `report:read:admin` (Para ver reportes de asistencia)
-   `user:read:admin` (Para listar a los docentes)
-   `dashboard:read:admin` (Opcional, para estadísticas)

Haz clic en **Continue** y asegúrate de que la App esté activada.

## Paso 4: Configurar Credenciales en n8n
1.  En n8n, ve a **Credentials** -> **New**.
2.  Busca **Zoom OAuth2 API**.
3.  **Grant Type:** Selecciona `Server-to-Server`.
4.  Copia los datos del Paso 2 (`Account ID`, `Client ID`, `Client Secret`).
5.  Haz clic en **Save**.

¡Listo! Ahora n8n tiene permiso para leer todo sin que inicies sesión manualmente.
