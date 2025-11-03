from models.producto import Producto
from repositories.producto_repo import ProductoRepository

repo = ProductoRepository()

async def agregar(producto: Producto):
    return await repo.create(producto.dict())

async def listar():
    productos = await repo.query({})
    return [p async for p in productos]

async def actualizar(id: str, producto: Producto):
    return await repo.update(id, producto.dict())

async def eliminar(id: str):
    return await repo.delete(id)
