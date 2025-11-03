from fastapi import APIRouter
from services import pedido_service as service

router = APIRouter(prefix="/pedido", tags=["Pedido"])

@router.post("/confirmar/{idUsuario}")
async def confirmar(idUsuario: str, total: float):
    return await service.confirmar(idUsuario, total)

@router.get("/{idUsuario}")
async def obtener(idUsuario: str):
    return await service.listar_por_usuario(idUsuario)

