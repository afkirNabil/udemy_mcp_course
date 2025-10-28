from fastmcp import FastMCP
import sqlite3
from typing import List, Dict, Any # Importamos tipos para documentar las funcionadidades/herramientas

# MCP Server Instance
mcp = FastMCP("Videogames Store")

DB_PATH = "C:\\Users\\NabilAS\\udemy\\mcp\\seccion3-bbdd-tienda-videojuegos\\tienda_videojuegos.db"

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect(DB_PATH)

# Tools Definition
# Usamos un decorador para definir una herramienta y que fastmcp la reconozca y no se piense q es una funcion auxiliar
# Hay q usar Type Hints cuando definimos una funcionalidad: parametros y tipos de parametros recibe y devuelve. Y una descripcion en Docstring. Esto es necesario para cuando el cliente le pase la descripicon de la funcion el llm sepa que tipo de dato generar y como funcion la herramienta.
@mcp.tool()
def listar_tablas() -> List[str]:
    """
    Lista todas las tablas disponibles en la base de datos.
    Útil para conocer la estructura de la base de datos antes de hacer consultas.
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table'
        ORDER BY name;
        """)
    tablas = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tablas

@mcp.tool()
def describir_tabla(nombre_tabla: str) -> Dict[str, Any]:
    """
    Obtiene información detallada sobre una tabla específica.
    Incluye columnas, tipos de datos y información del esquema.
    
    Args:
        nombre_tabla: Nombre de la tabla a describir
        
    Returns:
        Diccionario con el esquema de la tabla
    """
    conn = connect_db()
    cursor = conn.cursor()
    
    # Obtener información de columnas
    cursor.execute(f"PRAGMA table_info({nombre_tabla})")
    columnas = cursor.fetchall()
    
    # Obtener conteo de registros
    cursor.execute(f"SELECT COUNT(*) FROM {nombre_tabla}")
    total_registros = cursor.fetchone()[0]
    
    conn.close()
    
    esquema = {
        "nombre": nombre_tabla,
        "total_registros": total_registros,
        "columnas": [
            {
                "nombre": col[1],
                "tipo": col[2],
                "no_nulo": bool(col[3]),
                "valor_por_defecto": col[4],
                "es_clave_primaria": bool(col[5])
            }
            for col in columnas
        ]
    }
    
    return esquema

@mcp.tool()
def ejecutar_consulta(sql: str) -> List[Dict[str, Any]]:
    """
    Ejecuta una consulta SQL SELECT de solo lectura en la base de datos.
    
    IMPORTANTE: Solo se permiten consultas SELECT (lectura).
    No se permiten INSERT, UPDATE, DELETE, DROP, etc.
    
    Args:
        sql: Consulta SQL SELECT a ejecutar
        
    Returns:
        Lista de diccionarios con los resultados
    """
    # Validación de seguridad: solo permitir SELECT
    sql_upper = sql.strip().upper()
    if not sql_upper.startswith('SELECT'):
        return [{
            "error": "Solo se permiten consultas SELECT",
            "tipo": "SecurityError"
        }]
    
    # Palabras prohibidas para mayor seguridad
    palabras_prohibidas = ['DROP', 'DELETE', 'INSERT', 'UPDATE', 'ALTER', 'CREATE']
    if any(palabra in sql_upper for palabra in palabras_prohibidas):
        return [{
            "error": f"Consulta no permitida. Palabras prohibidas: {', '.join(palabras_prohibidas)}",
            "tipo": "SecurityError"
        }]
    
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(sql)
        
        # Obtener nombres de columnas
        columnas = [description[0] for description in cursor.description]
        
        # Convertir resultados a lista de diccionarios
        resultados = []
        for fila in cursor.fetchall():
            resultados.append(dict(zip(columnas, fila)))
        
        conn.close()
        
        return resultados
    
    except sqlite3.Error as e:
        return [{
            "error": str(e),
            "tipo": "SQLError"
        }]

# Start Point
if __name__ == "__main__":
    mcp.run() #stdio, corrienod en local en la misma maquina
    # mcp.run(transport="http", host="127.0.0.1", port=8080, path="/mcp") # corriendo en servidor http local o en otra maquina de la red