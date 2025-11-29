from bson import ObjectId
from config import db

class BoletaRepository:
    collection = db["boletas"]

    async def crear(self, boleta):
        result = await self.collection.insert_one(boleta)
        boleta["id"] = str(result.inserted_id) 
        return boleta

    async def obtener(self, id: str):
        boleta = await self.collection.find_one({"_id": ObjectId(id)})
        if boleta:
            boleta["id"] = str(boleta["_id"])
            del boleta["_id"]
        return boleta

    async def listar_por_usuario(self, idUsuario: str):
        cursor = self.collection.find({"idUsuario": idUsuario})
        boletas = []
        async for b in cursor:
            b["id"] = str(b["_id"])
            del b["_id"]
            boletas.append(b)
        return boletas

    async def eliminar(self, id: str):
        await self.collection.delete_one({"_id": ObjectId(id)})
        return True

    async def actualizar_estado(self, id: str, nuevo_estado: str):
        await self.collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"estado": nuevo_estado}}
        )
        return True


