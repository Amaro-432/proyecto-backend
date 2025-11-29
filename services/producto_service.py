from repositories.producto_repo import ProductoRepository

repo = ProductoRepository()

async def crear_producto(producto):
    return await repo.create(producto.dict())

async def listar_productos(categoria=None, precio_min=None, precio_max=None):
    return await repo.get_all(categoria, precio_min, precio_max)

async def obtener_producto(id):
    return await repo.get_by_id(id)

async def actualizar_producto(id, data):
    return await repo.update(id, data.dict())

async def eliminar_producto(id):
    return await repo.delete(id)
