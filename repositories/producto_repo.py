from config import db
from repositories.icrud import ICRUD
from bson import ObjectId

class ProductoRepository(ICRUD):

    collection = db["productos"]

    async def create(self, producto):
        result = await self.collection.insert_one(producto)
        return str(result.inserted_id)

    async def get(self, id):
        return await self.collection.find_one({"_id": ObjectId(id)})

    async def query(self, filtro):
        return self.collection.find(filtro)

    async def update(self, id, data):
        await self.collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        return True

    async def delete(self, id):
        await self.collection.delete_one({"_id": ObjectId(id)})
        return True
