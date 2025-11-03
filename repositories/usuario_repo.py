from config import db
from repositories.icrud import ICRUD
from bson import ObjectId

class UsuarioRepository(ICRUD):

    collection = db["usuarios"]

    async def create(self, usuario):
        result = await self.collection.insert_one(usuario)
        return str(result.inserted_id)

    async def get(self, id):
        return await self.collection.find_one({"_id": ObjectId(id)})

    async def query(self, correo):
        return await self.collection.find_one({"correo": correo})

    async def update(self, id, data):
        await self.collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        return True

    async def delete(self, id):
        await self.collection.delete_one({"_id": ObjectId(id)})
        return True
    
    async def findByEmail(self, email: str):
        return await self.collection.find_one({"email": email})

