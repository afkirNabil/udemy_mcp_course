# Sección 5: Clientes MCP Personalizados y Gestor de Correo Inteligente

En esta sección del curso, nos enfocamos en la creación de **Clientes MCP (Model Context Protocol)** con interfaces gráficas profesionales y la implementación de un servior MCP completo para la gestión de correos electrónicos con Gmail.

Aprenderás a consumir herramientas, recursos y prompts desde tu propia aplicación web construida con Streamlit.

## 📂 Contenido del Proyecto

*   **`app.py`**: Interfaz de usuario desarrollada con Streamlit. Actúa como el Cliente MCP que conecta con el servidor y ofrece una experiencia de chat interactiva al usuario.
*   **`client.py`**: Lógica del cliente MCP. Maneja la conexión con el servidor, el procesamiento de mensajes y la integración con el modelo LLM (GPT-4o-mini).
*   **`manuals/`**: Carpeta que contiene manuales en PDF que el servidor expone como recursos dinámicos.

## 🚀 Funcionalidades

### 1. Cliente MCP Gráfico (Streamlit)
*   **Chat Interactivo:** Conversa con el asistente para gestionar tus correos.
*   **Visualización de Recursos:** Explora las herramientas y recursos disponibles en el servidor directamente desde la barra lateral.
*   **Renderizado de Componentes:** Respuestas ricas con formato Markdown y componentes visuales para resultados de herramientas.

### 2. Servidor MCP de Gmail
*   **Herramientas (`Tools`):**
    *   `list_emails`: Lista correos recientes con filtros.
    *   `send_email`: Envía correos electrónicos nuevos.
*   **Recursos (`Resources`):**
    *   `gmail://profile`: Información del perfil de usuario.
    *   `docs://setup-manual/{version}`: Acceso dinámico a manuales PDF.
*   **Prompts:**
    *   `daily_email_summary`: Plantilla predefinida para resumir emails urgentes y pendientes.
    *   `compose_professional_email`: Asistente para redactar correos formales.

## 🛠️ Configuración y Ejecución

### Requisitos Previos

Asegúrate de estar en el entorno virtual del proyecto y tener las dependencias instaladas (ver `requirements.txt` en la raíz del repositorio).

Necesitarás:
1.  **API Key de OpenAI:**
2.  **Credenciales de Google:**

### Ejecución

Para iniciar la aplicación web (Cliente MCP):

```bash
streamlit run app.py
```

*Nota: La aplicación iniciará automáticamente el servidor MCP (`gmail_mcp_server.py`) en segundo plano para establecer la conexión.*

## 💡 Uso

1.  Al abrir la aplicación, verás el panel lateral con la información del sistema MCP (herramientas y recursos conectados).
2.  Usa los botones de **"Prompts Rápidos"** para acciones comunes como "Resumen diario".
3.  Escribe en el chat natural para pedirle al asistente que lea tus correos, busque información o redacte respuestas.

---
*Este proyecto demuestra cómo MCP permite desacoplar la lógica del servidor (Gmail) de la interfaz de usuario (Streamlit), usando LLMs como puente inteligente.*
