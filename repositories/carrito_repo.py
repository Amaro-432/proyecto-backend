from motor.motor_asyncio import AsyncIOMotorDatabase

class CarritoRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.col = db["carritos"]

    async def find_by_user(self, user_id: str):
        """
        Busca el carrito de un usuario. Si no existe, lo crea vacío.
        """
        carrito = await self.col.find_one({"user_id": user_id})
        if not carrito:
            carrito = {"user_id": user_id, "items": []}
            await self.col.insert_one(carrito)
        return carrito

    async def add_item(self, user_id: str, id_producto: str, cantidad: int, producto: dict):
        """
        Agrega un producto al carrito. Si ya existe, actualiza la cantidad.
        """
        carrito = await self.find_by_user(user_id)
        items = carrito.get("items", [])

        found = False
        for it in items:
            if it["idProducto"] == id_producto:
                it["cantidad"] = int(cantidad)   # puedes sumar en vez de reemplazar
                found = True
                break

        if not found:
            # producto ya viene enriquecido con nombre, precio, imagen
            items.append({
                "idProducto": id_producto,
                "nombre": producto.get("nombre"),
                "precio": producto.get("precio"),
                "imagen": producto.get("imagen"),
                "cantidad": int(cantidad)
            })

        await self.col.update_one(
            {"user_id": user_id},
            {"$set": {"items": items}}
        )
        return {"ok": True}

    async def remove_item(self, user_id: str, id_producto: str):
        """
        Elimina un producto del carrito.
        """
        carrito = await self.find_by_user(user_id)
        items = [it for it in carrito.get("items", []) if it["idProducto"] != id_producto]

        await self.col.update_one(
            {"user_id": user_id},
            {"$set": {"items": items}}
        )
        return {"ok": True}

