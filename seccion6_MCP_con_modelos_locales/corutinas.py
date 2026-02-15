import asyncio

async def conectar():
    print("Conectando al servidor...")
    await asyncio.sleep(2)  # Simula una espera
    print("Conexión establecida")
    # return "cliente"

async def main():
    async with await conectar() as cliente:  # Esto en tu caso sería un objeto con __aenter__
        print("Listando herramientas...")
        await asyncio.sleep(1)
        print("Herramientas listadas")

# Ejecutar
asyncio.run(main())
