# Sección 3: Sistema de Base de Datos - Tienda de Videojuegos

En esta sección construimos un **Servidor MCP** capaz de interactuar con una base de datos SQLite. El objetivo es permitir que un LLM consulte información estructurada sobre el catálogo de una tienda de videojuegos de forma segura.

## 📂 Contenido del Proyecto

*   **`mcp_server.py`**: Servidor MCP que implementa herramientas para explorar y consultar la base de datos.
*   **`tienda_videojuegos.db`**: Base de datos SQLite precargada con tablas de juegos, clientes y ventas.
*   **`claude_desktop_config.json`**: Ejemplo de configuración para integrar este servidor con la aplicación de escritorio de Claude.

## 🚀 Funcionalidades (Tools)

El servidor expone tres herramientas principales para la exploración de datos:

### 1. `listar_tablas()`
*   **Descripción:** Devuelve una lista de todas las tablas existentes en la base de datos.
*   **Uso:** Es el primer paso para que el LLM "entienda" qué información está disponible.

### 2. `describir_tabla(nombre_tabla)`
*   **Descripción:** Proporciona el esquema detallado de una tabla (nombres de columnas, tipos de datos, claves primarias).
*   **Argumentos:**
    *   `nombre_tabla`: El nombre de la tabla a inspeccionar.

### 3. `ejecutar_consulta(sql)`
*   **Descripción:** Permite ejecutar consultas SQL personalizadas.
*   **Seguridad:** Implementa restricciones de seguridad (modo **solo lectura**) bloqueando comandos como `INSERT`, `UPDATE`, `DELETE` o `DROP` para proteger la integridad de los datos.
*   **Argumentos:**
    *   `sql`: La sentencia `SELECT` a ejecutar.

## 🛠️ Configuración y Uso

### Ejecución con UV

Para iniciar el servidor localmente:

```bash
uv run mcp_server.py
```

### Integración con Claude Desktop

Para conectar este servidor a Claude, edita tu archivo de configuración (`claude_desktop_config.json`) añadiendo la entrada correspondiente.

**Ejemplo de configuración:**

```json
"DBVideogamesStore": {
  "command": "uv",
  "args": [
    "--directory",
    "RUTA_ABSOLUTA_A_ESTA_CARPETA",
    "run",
    "mcp_server.py"
  ]
}
```

También puedes usar el servidor oficial de SQLite directamente (`mcp-server-sqlite`) como se muestra en el archivo de configuración de ejemplo incluido, pero este script `mcp_server.py` demuestra cómo crear una implementación personalizada con lógica de seguridad propia.
