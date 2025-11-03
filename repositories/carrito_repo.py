from config import db

class CarritoRepository:
    collection = db["carritos"]

    async def obtener(self, idUsuario):
        carrito = await self.collection.find_one({"idUsuario": idUsuario})
        if carrito:
            return carrito
        # si no existe, se crea uno vacío
        await self.collection.insert_one({"idUsuario": idUsuario, "items": []})
        return {"idUsuario": idUsuario, "items": []}

    async def actualizar(self, idUsuario, carrito):
        await self.collection.update_one({"idUsuario": idUsuario}, {"$set": carrito})
        return True
