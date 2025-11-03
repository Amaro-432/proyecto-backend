from passlib.context import CryptContext
from repositories.usuario_repo import UsuarioRepository
from auth.jwt_handler import crear_token

repo = UsuarioRepository()
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def registrar(usuario):
    usuario.password = pwd.hash(usuario.password)
    return await repo.create(usuario.dict())

async def login(email: str, password: str):
    user = await repo.findByEmail(email)

    if not user or not pwd.verify(password, user["password"]):
        return {"error": "Credenciales inválidas"}

    token = crear_token({"id": str(user["_id"]), "rol": user["rol"]})
    return {"token": token, "rol": user["rol"]}
