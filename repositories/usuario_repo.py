from config import db
from bson import ObjectId
from repositories.icrud import ICRUD


class UsuarioRepository(ICRUD):

    collection = db["usuarios"]

    async def create(self, usuario):
        result = await self.collection.insert_one(usuario)
        usuario["_id"] = str(result.inserted_id)
        return usuario

    async def get(self, id):
        return await self.collection.find_one({"_id": ObjectId(id)})

    async def query(self, email):
        return await self.collection.find_one({"email": email})

    async def update(self, id, data):
        await self.collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        return True

    async def delete(self, id):
        await self.collection.delete_one({"_id": ObjectId(id)})
        return True

    async def find_by_email(self, email: str):
        """
        Retorna el usuario tal como está en la BD (SIN serializar).
        Esto es importante para que passlib pueda verificar correctamente el hash.
        """
        return await self.collection.find_one({"email": email})
    async def actualizar_perfil(self, id, perfil_data):
        result = await self.collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"perfil": perfil_data}}
        )
        return {"msg": "Perfil actualizado correctamente", "modified_count": result.modified_count}
    
    async def listar_todos(self):
        cursor = self.collection.find({})
        usuarios = []
        async for u in cursor:
            u["_id"] = str(u["_id"])  # serializar ObjectId
            usuarios.append(u)
        return usuarios

