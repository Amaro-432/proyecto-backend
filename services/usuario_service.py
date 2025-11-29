from models.usuario import Usuario
from repositories.usuario_repo import UsuarioRepository
from models.perfil import Perfil
from utils.mongo_helpers import serialize_doc


repo = UsuarioRepository()

async def registrar(usuario: Usuario):
    existe = await repo.query(usuario.email)
    if existe:
        return {"status": "error", "msg": "Correo ya registrado"}

    uid = await repo.create(usuario.dict())
    return {"status": "ok", "id": uid}

async def login(email, password):
    usuario = await repo.find_by_email(email)
    if not usuario:
        return None

    if not pwd.verify(password, usuario["password"]):
        return None

    usuario = serialize_doc(usuario)
    del usuario["password"]
    return usuario

async def obtener_perfil(idUsuario: str):
    usuario = await repo.get(idUsuario)
    if usuario and "perfil" in usuario:
        return usuario["perfil"]
    return None

async def actualizar_perfil(idUsuario: str, perfil: Perfil):
    return await repo.actualizar_perfil(idUsuario, perfil.dict())

async def listar_usuarios():
    usuarios = await repo.listar_todos()
    # opcional: remover contraseñas antes de devolver
    for u in usuarios:
        if "password" in u:
            del u["password"]
    return usuarios

async def listar_por_rol(rol: str):
    usuarios = await repo.listar_todos()
    usuarios_filtrados = [u for u in usuarios if u.get("rol") == rol]
    return usuarios_filtrados


async def actualizar_usuario(idUsuario: str, data: dict):
    if "password" in data:
        del data["password"]  # no permitir cambio directo aquí
    return await repo.update(idUsuario, data)

async def eliminar_usuario(idUsuario: str):
    return await repo.delete(idUsuario)

