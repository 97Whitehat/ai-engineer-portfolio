import asyncio, time


async def obtener_precio(ticker):
    await asyncio.sleep(1)
    return 100.0

async def main(): #tiempo de ejecución 1.02s
    precio1, precio2, precio3 = await asyncio.gather(
        obtener_precio("AAPL"),
        obtener_precio("OWND"),
        obtener_precio("GHJK"),
    )
    print(precio1, precio2, precio3)


# async def main(): tiempo de ejecución 3.02s
#     inicio = time.time()
#     precio1 = await obtener_precio("AAPL")
#     precio2 = await obtener_precio("OWND")
#     precio3 = await obtener_precio("GHJK")
#     print(precio1, precio2, precio3)
#     fin = time.time()
#     print(f"Tiempo total: {fin - inicio:.2f} segundos")

inicio = time.time()
asyncio.run(main())
fin = time.time()
print(f'Tiempo total: {fin -inicio:.2f} segundos')