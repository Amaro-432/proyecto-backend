from fastapi import APIRouter
from pydantic import BaseModel
from models.usuario import Usuario, LoginRequest
from services import auth_service as service

router = APIRouter(prefix="/auth", tags=["Autenticación"])

class LoginData(BaseModel):
    email: str
    password: str

@router.post("/register")
async def registrar(usuario: Usuario):
    result = await service.registrar(usuario)

    if result.get("error") == "NOMBRE_VACIO":
        return {"error": "Debe ingresar un nombre válido"}

    if result.get("error") == "EMAIL_EXISTE":
        return {"error": "Correo ya registrado"}

    return result


@router.post("/login")
async def login(data: LoginData):
    result = await service.login(data.email, data.password)

    if not result:
        return {"error": "Credenciales inválidas"}

    return result