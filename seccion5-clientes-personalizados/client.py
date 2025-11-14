from fastmcp import Client

class GmailMCPClient:
    def __init__(self):
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