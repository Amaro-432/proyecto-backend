from models.usuario import Usuario
from repositories.usuario_repo import UsuarioRepository

repo = UsuarioRepository()

async def registrar(usuario: Usuario):
    existe = await repo.query(usuario.correo)
    if existe:
        return {"status": "error", "msg": "Correo ya registrado"}

    uid = await repo.create(usuario.dict())
    return {"status": "ok", "id": uid}

async def login(correo: str, passw: str):
    user = await repo.query(correo)
    if user and user["passw"] == passw:
        return {"status": "ok", "usuario": user["nombre"], "perfil": user["perfil"]}
    return {"status": "error", "msg": "Credenciales inválidas"}
