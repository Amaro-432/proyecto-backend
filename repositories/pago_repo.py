from config import db
from bson import ObjectId

class PagoRepository:
    collection = db["pagos"]

    async def crear(self, pago):
        result = await self.collection.insert_one(pago)
        return str(result.inserted_id)

    async def confirmar(self, idPago):
        await self.collection.update_one({"_id": ObjectId(idPago)}, {"$set": {"estado": "confirmado"}})
        return True
