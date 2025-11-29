from config import db
from bson import ObjectId

class PagoRepository:
    collection = db["pagos"]

    async def crear(self, pago):
        result = await self.collection.insert_one(pago)
        return str(result.inserted_id)

    async def confirmar(self, idPago):
        await self.collection.update_one(
            {"_id": ObjectId(idPago)},
            {"$set": {"estado": "confirmado"}}
        )
        return True
    
    async def find_by_token(self, token):
        return await self.collection.find_one({"token": token})

# Instancia para importar como 'pago_repo'
pago_repo = PagoRepository()

# Opcional: facilitar debugging
__all__ = ["pago_repo", "PagoRepository"]

