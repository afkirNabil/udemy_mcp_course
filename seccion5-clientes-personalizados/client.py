from fastmcp import Client
from openai import OpenAI
from dotenv import load_dotenv
import os

# Busca el archivo .env y carga esta variable como una variable de entrono.
load_dotenv()

class GmailMCPClient:
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.mcp_server_path = "C:\\Users\\NabilAS\\udemy\\mcp\\seccion5-clientes-personalizados\\gmail_mcp_server.py"
        # Ruta al Servidor MCP q va a consultar/conectarse este Cliente.
        # Aqui podriamos conectarnos a un servidor remorto mediante URL. Pero en nuestro caso usamor uno servidor perosnalizado local.

    async def _get_mcp_client(self):
        """Inicializar y crea conexión con el servidor MCP"""
        return Client(self.mcp_server_path)
    
    async def get_system_info(self) -> dict:
        """Información del sistema/Servidor MCP"""
        async with await self._get_mcp_client() as cliente:
            # Tenemos q esperar a q se cree la conexion con el servidor MCP???
            tools = await cliente.list_tools()
            # Con el await le indico q no espero por el metodo al q invoca, sino q pase a ejecutar los otros metodos del Client MCP con alias Cliente
            resources = await cliente.list_resources()
            templates = await cliente.list_resource_templates()
            prompts = await cliente.list_prompts()

            return {
                "tools": [t.name for t in tools],
                # list comprehension
                "resources": [r.name for r in resources],
                "templates": [t.name for t in templates],
                "prompts": [p.name for p in prompts],
                "server": self.mcp_server_path
            }
        
    async def get_tools_for_openai(self):
        """Convierte herramientas del Servidor MCP al formato de OpenAI para mandar esas herramientas al modelo GPT-4o-mini"""
        async with await self._get_mcp_client() as cliente:
        # async with: el objeto cliente es un "context manager asincrono". Define metodos espaciales. Sirve para manejar correctamente recursos sin bloquar el programa
            tools = await cliente.list_tools()

            openai_tools = []
            for tool in tools:
                openai_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description or "",
                        "parameters": tool.inputSchema
                    }
                })
            
            return openai_tools, cliente
        
    async def get_resources_as_tools(self):
        """Encapsula recursos y templates como herramientas."""
        async with await self._get_mcp_client() as cliente:
            # Obtener recursos y templates
            resources = await cliente.list_resources()
            templates = await cliente.list_resource_templates()

            # Convertir/encapsular los recursos y plantillas en funciones/herramientas de OpenAi para su modelo gpt 5.
            # Para guardar los recursos.
            resource_tools = []
            # mapeo con nombre del recurso y su descripcion para volver a la forma incial del recurso (pq lo vamos a convertir a funcion) cuando el modelo LLM quiera hacer uso de ese recurso. El cliente se comunica con el servidor mediante formato json rpc.
            resource_map = {}

            # 1. Recursos estáticos
            for resource in resources:
                uri = str(resource.uri)
                # Obtener el nombre de la herramienta desde la uri para q le funcion/herramienta del modelo llm tenga ese mismo nombre.
                func_name = f"get_resource_{uri.replace('://', '_').replace('/', '_')}"

                # Convertir el propio recurso en una funcion/herramienta con el formato de openai para su modelo gpt.
                resource_tools.append({
                    "type": "function",
                    "function": {
                        "name": func_name,
                        "description": resource.description or resource.name,
                        "parameters": {"type": "object", "properties": {}, "required": []}
                        # al ser recursos estaticos no necesitan argumentos ni parametros, aqui indicamos q no tiene parametros.
                    }
                })

                resource_map[func_name] = {"uri": uri}

            # 2. Resource templates
            for template in templates:
                uri_template = str(template.uriTemplate)
                func_name = template.name

                # Extraer parametros del template. Pq contiene variables dinámicas.
                import re
                params = re.findall(r'\{(\w+)\}', uri_template)

                # Diccionario con las propiedades de los parametros de las rutas dinamicas de las plantillas.
                # Este diccionario hay q pasarselo a openAI.
                # Dict Comprehension.
                properties = {p: {"type": "string", "description": f"Parametro {p}"} for p in params}

                # Formato OpenAi de Herramientas/Funciones.
                resource_tools.append({
                    "type": "function",
                    "function": {
                        "name": func_name,
                        "description": template.description or template.name,
                        "parameters": {
                            "type": "object",
                            "properties": properties,
                            "required": params
                        }
                    }
                })

                # resource_map[func_name] = {"template": uri_template, "params": params}
                resource_map[func_name] = {"uri_template": uri_template, "params": params}
            
            return resource_tools, resource_map
        
    # Al obtener los prompts es diferente tienes q saber a priori a cual vas a llamar. Esto es pq vamos a tener botones en la interfaz gráfica para cada prompt.
    async def get_prompt_messages(self, prompt_name: str, **kwargs) -> str:
        """Obtiene el mensaje de un prompt especifico."""
        async with await self._get_mcp_client() as cliente:
            prompt = await cliente.get_prompt(prompt_name, arguments=kwargs)
            # interpretamos el diccionario text con eval
            return eval(prompt.messages[0].content.text)
        
    async def call_tool(self, tool_name: str, arguments: dict, client):
        """Ejecuta una herramienta MCP cuando lo solicite el LLM"""
        result = await client.call_tool(tool_name, arguments)
        # Verificar la estructura de la respuesta
        if result and result.content and len(result.content) > 0:
            if hasattr(result.content[0], 'text'):
                # Respuesta de ejecutar la herramienta
                return result.content[0].text
        return "Herramienta ejecutada sin resultados"
    
    async def get_resource(self, uri: str, client):
        """Obtiene un recurso MCP cuando lo solicite el LLM"""
        result = await client.read_resource(uri)
        # Verificar estructura de la respuesta
        if result and len(result) > 0:
            if hasattr(result[0], 'text'):
                return result[0].text
            elif hasattr(result[0], 'content'):
                return result[0].content
        return "Recurso no disponible"
    
    # messages: list es el historial de la conversacion
    # le mandamos todo el historial para q el llm tenga contexto y el llm añade el ultimo mensaje.
    async def chat(self, messages: list) -> str:
        """Procesa una conversación con GPT utilizando MCP"""
        async with await self._get_mcp_client() as mcp_client:
            # Obtener herramientas y recursos
            # la barra baja desecha el cliente (variable) q nos devuelve el metodo pq ya hemos conectado otro cliente llamado mcp. 
            tools, _ = await self.get_tools_for_openai()
            resource_tools, resource_map = await self.get_resources_as_tools()
            # En el primer mensaje le mandamos al llm todas las herramientas y los recursos encapsulados.
            all_tools = tools + resource_tools

            # LLamada inicial a OpenAI, cliente inicializado en el init de la Clase.
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=all_tools,
                tool_choice="auto"
            )

            # Comprobar que existe una function call en la respuesta del LLM, que seria un JSON. Si es texto, pues no seria una llamada a una herramienta.
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            # Si no hay tool calls, retornar respuesta directa
            if not tool_calls:
                return response_message.content

            # LLM intenta invocar una herramienta externa.
            # Processar tool calls

            # Vamos a añadir la respuesta (herramientas) del LLM al chat. Ya que la necesitamos para guardarla en el estado globar de la app.
            messages.append({
                "role": "assistant",
                "content": response_message.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in tool_calls
                ]
            })

            # Comprobar cuales son esas llamadas a funciones y herramientas e invocarlas.
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                # Con eval los interpreto y obtener en forma de diccionario.
                function_args = eval(tool_call.function.arguments)

                # Verficar si es un recurso
                if function_name in resource_map:
                    resource_info = resource_map[function_name]

                    # Comprobar si es un recurso estatico o una plantilla.
                    if "uri_template" in resource_info:
                        # Resource template: construir URI
                        uri = resource_info["uri_template"]
                        for param in resource_info["params"]:
                            uri = uri.replace(f"{{{param}}}", str(function_args.get(param, "")))
                    else:
                        # Recurso estatico
                        uri = resource_info['uri']

                    function_response = await self.get_resource(uri, mcp_client)

                # Herramienta normal
                else:
                    function_response = await self.call_tool(function_name, function_args, mcp_client)

                # Componer el mensaje de respuesta al LLM, formato OpenAI.
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response
                })

                # Segunda llamada con resultados de la herramienta
                second_response = self.openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages
                )
                
                return second_response.choices[0].message.content