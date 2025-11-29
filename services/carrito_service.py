from repositories.carrito_repo import CarritoRepository
from repositories.producto_repo import ProductoRepository
from repositories.usuario_repo import UsuarioRepository
from config import db

carrito_repo = CarritoRepository(db)
producto_repo = ProductoRepository()

async def obtener(user_id: str):
    carrito = await carrito_repo.find_by_user(user_id)
    return {"items": carrito.get("items", [])}

async def agregar(user_id: str, id_producto: str, cantidad: int):
    # ⚠️ usar get_by_id en lugar de find_by_id
    prod = await producto_repo.get_by_id(id_producto)
    if not prod:
        return {"error": "PRODUCTO_NO_ENCONTRADO"}

    # Enriquecer el carrito con los campos del modelo Producto
    producto = {
        "idProducto": str(prod["_id"]),
        "nombre": prod["nombre"],
        "precio": prod["precio"],
        "imagen": prod.get("imagen"),
        "cantidad": cantidad
    }

    await carrito_repo.add_item(user_id, id_producto, cantidad, producto)
    return await obtener(user_id)

async def eliminar(user_id: str, id_producto: str):
    await carrito_repo.remove_item(user_id, id_producto)
    return await obtener(user_id)

