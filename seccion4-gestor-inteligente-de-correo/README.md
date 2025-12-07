# Sección 4: Servidor MCP - Gestor Inteligente de Correo

En esta sección desarrollamos un **Servidor MCP** completo dedicado a la gestión de correos electrónicos utilizando la API de Gmail.

Aquí nos centramos en la arquitectura backend del servidor MCP, utilizando `fastmcp` para definir herramientas y recursos, y `uv` para la gestión moderna de dependencias.

## 📂 Estructura del Proyecto

*   **`gmail_mcp_server.py`**: El núcleo del servidor MCP. Define:
    *   **Tools**: Funcionalidades para interactuar con Gmail (listar correos, enviar mensajes).
    *   **Resources**: Datos expuestos de solo lectura (perfil de usuario, manuales PDF).
    *   **Prompts**: Plantillas predefinidas para ayudar a los LLMs a usar las herramientas eficazmente.
*   **`pyproject.toml` / `uv.lock`**: Definición de dependencias y configuración del proyecto gestionado con `uv`.
*   **`manuals/`**: Directorio con documentación (PDFs) expuesta dinámicamente como recursos.

## 🚀 Funcionalidades del Servidor

### Herramientas (Tools)
*   `list_emails(max_results=10, query="")`: Busca y lista correos recientes. Soporta filtros de búsqueda de Gmail (ej. "is:unread").
*   `send_email(to, subject, body)`: Envía correos electrónicos a través de la API de Gmail.

### Recursos (Resources)
*   `gmail://profile`: Devuelve información del usuario conectado (total de mensajes, email, etc.).
*   `docs://setup-manual/{version}`: Lee y devuelve el contenido de manuales PDF locales según la versión solicitada.

### Prompts
*   `daily_email_summary`: Instruye al LLM para generar un resumen ejecutivo de los correos importantes del día.
*   `compose_professional_email`: Guía al LLM para redactar correos formales paso a paso y enviarlos.

## 🛠️ Configuración y Ejecución

Este proyecto utiliza **uv** para una gestión de entornos rápida y eficiente.

### Requisitos Previos
1.   Tener `uv` instalado.
2.   Disponer del archivo de credenciales de Google (`credentials-gmail-scopes.json`) en la raíz del directorio (necesario para la primera autenticación).

### Ejecutar el Servidor

Puedes ejecutar el servidor en modo desarrollo o inspección:

```bash
# Ejecutar directamente con python (usando el entorno de uv)
uv run gmail_mcp_server.py

# Inspeccionar el servidor con MCP Inspector (muy útil para depurar)
npx @modelcontextprotocol/inspector uv run gmail_mcp_server.py
```

### Conectar con Claude Desktop

Para usar este servidor con Claude Desktop, añade la configuración a tu archivo `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "gmail-manager": {
      "command": "uv",
      "args": [
        "--directory",
        "RUTA_ABSOLUTA_A_ESTA_CARPETA",
        "run",
        "gmail_mcp_server.py"
      ]
    }
  }
}
```
