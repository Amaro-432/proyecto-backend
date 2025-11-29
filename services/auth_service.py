import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from repositories.usuario_repo import UsuarioRepository

SECRET_KEY = "clave-super-secreta"
ALGORITHM = "HS256"

repo = UsuarioRepository()

pwd = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

async def registrar(usuario):
    if not usuario.nombre or usuario.nombre.strip() == "":
        return {"error": "NOMBRE_VACIO"}

    existente = await repo.find_by_email(usuario.email)
    if existente:
        return {"error": "EMAIL_EXISTE"}

    data = usuario.dict()
    if "rol" not in data or not data["rol"]:
        data["rol"] = "cliente"

    data["password"] = pwd.hash(data["password"])
    return {"ok": True, "usuario": await repo.create(data)}

async def login(email, password):
    usuario = await repo.find_by_email(email)
    if not usuario:
        return None

    if not pwd.verify(password, usuario["password"]):
        return None

    # Crear token JWT con exp como timestamp
    payload = {
        "sub": str(usuario["_id"]),
        "email": usuario["email"],
        "rol": usuario["rol"],
        "exp": int((datetime.utcnow() + timedelta(hours=12)).timestamp())
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "usuario": {
            "id": str(usuario["_id"]),
            "nombre": usuario["nombre"],
            "email": usuario["email"],
            "rol": usuario["rol"]
        },
        "token": token
    }
