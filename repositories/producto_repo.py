from config import db
from bson import ObjectId
from utils.mongo_helpers import serialize_doc

class ProductoRepository:

    collection = db["productos"]

    async def create(self, data):
        result = await self.collection.insert_one(data)
        data["_id"] = str(result.inserted_id)
        return data

    async def get_all(self, categoria=None, precio_min=None, precio_max=None):
        filtro = {}

        if categoria and categoria != "Todos":
            filtro["categoria"] = categoria

        if precio_min is not None or precio_max is not None:
            filtro["precio"] = {}
            if precio_min is not None:
                filtro["precio"]["$gte"] = precio_min
            if precio_max is not None:
                filtro["precio"]["$lte"] = precio_max

        productos = []
        async for doc in self.collection.find(filtro):
            productos.append(serialize_doc(doc))
        return productos
    

    async def get_by_id(self, id):
        producto = await self.collection.find_one({"_id": ObjectId(id)})
        return serialize_doc(producto) if producto else None

    async def update(self, id, data):
        await self.collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        return True

    async def delete(self, id):
        await self.collection.delete_one({"_id": ObjectId(id)})
        return True
    
   


