from fastapi import APIRouter
from models.usuario import Usuario
from services import auth_service as service

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/register")
async def registrar(usuario: Usuario):
    return await service.registrar(usuario)

@router.post("/login")
async def login(email: str, password: str):
    return await service.login(email, password)
