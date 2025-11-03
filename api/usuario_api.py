from fastapi import APIRouter
from models.usuario import Usuario
from services.usuario_service import registrar, login

router = APIRouter(prefix="/usuario", tags=["Usuario"])

@router.post("/registro")
async def registro(usuario: Usuario):
    return await registrar(usuario)

@router.post("/login")
async def iniciar_sesion(correo: str, passw: str):
    return await login(correo, passw)

