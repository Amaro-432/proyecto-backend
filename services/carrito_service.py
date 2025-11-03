from repositories.carrito_repo import CarritoRepository

repo = CarritoRepository()

async def agregar(idUsuario: str, idProducto: str, cantidad: int):
    carrito = await repo.obtener(idUsuario)

    # verificar si el producto ya estaba en el carrito
    for item in carrito["items"]:
        if item["idProducto"] == idProducto:
            item["cantidad"] += cantidad
            await repo.actualizar(idUsuario, carrito)
            return carrito

    carrito["items"].append({"idProducto": idProducto, "cantidad": cantidad})
    await repo.actualizar(idUsuario, carrito)
    return carrito

async def eliminar(idUsuario: str, idProducto: str):
    carrito = await repo.obtener(idUsuario)
    carrito["items"] = [i for i in carrito["items"] if i["idProducto"] != idProducto]
    return await repo.actualizar(idUsuario, carrito)
