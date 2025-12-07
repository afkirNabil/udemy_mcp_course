# Curso Práctico de Model Context Protocol (MCP)

Este repositorio agrupa implementaciones prácticas del curso de **Model Context Protocol (MCP)**, diseñado para dominar la integración de Grandes Modelos de Lenguaje (LLMs) con sistemas y datos del mundo real.

### 🎯 Objetivo del Repositorio

Demostrar la capacidad de construir **Arquitecturas de Agentes** robustas donde modelos como Claude, ChatGPT u Ollama pueden leer bases de datos, gestionar archivos, enviar correos y ejecutar acciones seguras a través de servidores MCP personalizados.

### 📂 Proyectos Principales

*   **Servidores MCP Backend:** Implementaciones con Python (`fastmcp`, `uv`) para exponer APIs y bases de datos SQLite a los LLMs.
*   **Clientes con Interfaz Gráfica:** Aplicaciones web en **Streamlit** que actúan como clientes MCP, permitiendo interacción humana fluida con las herramientas.
*   **Automatización Real:** Sistemas como un **Gestor Inteligente de Correo** (Gmail) y una **Base de Datos de Tienda** consultable en lenguaje natural.
*   **Seguridad:** Implementación de prácticas de autenticación y control de acceso en entornos de IA.

### Tecnologías usadas

*   Model Context Protocol (MCP) - arquitectura completa
*   Claude Desktop y ChatGPT - integración avanzada
*   Python con UV para gestión de entornos
*   Streamlit para interfaces web profesionales
*   OpenAI API y Ollama para LLMs
*   JWT y criptografía para seguridad
*   VS Code y MCP Inspector para desarrollo
*   Bases de datos y APIs REST

## 🚀 Instalación y Configuración

Sigue estos pasos para configurar el entorno de desarrollo en tu máquina local.

### 1. Clonar el Repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_DIRECTORIO>
```

### 2. Crear un Entorno Virtual

Se recomienda usar un entorno virtual para gestionar las dependencias.

**Windows:**

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar Dependencias

Instala todas las librerías necesarias con el archivo `requirements.txt` incluido en este repositorio:

```bash
pip install -r requirements.txt
```

## 🛠️ Cómo Correr los Proyectos

Cada sección del curso tiene su propia carpeta y scripts específicos. Asegúrate de tener el entorno virtual activado antes de ejecutar cualquier script.

Ejemplo general para ejecutar un servidor MCP o un script de Python:

```bash
python ruta/al/script.py
```

O si utilizas herramientas específicas como Streamlit o UV (según se indique en cada sección):

```bash
streamlit run ruta/al/app.py
# o
uv run ruta/al/script.py
```

*Consulta los `README.md` específicos dentro de cada carpeta de sección (si los hay) para instrucciones detalladas por proyecto.*

---
*Este repositorio es parte del curso práctico sobre Model Context Protocol.*
