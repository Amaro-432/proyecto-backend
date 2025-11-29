from fastapi import APIRouter
from pydantic import BaseModel
from services import pedido_service as service
from fastapi import Depends, HTTPException
from auth.dependencies import usuario_actual


router = APIRouter(prefix="/pedido", tags=["Pedido"])

class ConfirmarPedidoRequest(BaseModel):
    total: float

@router.post("/confirmar")
async def confirmar(req: ConfirmarPedidoRequest, usuario=Depends(usuario_actual)):
    # usar sub directamente, porque es lo que devuelve usuario_actual
    return await service.confirmar(usuario["sub"], req.total)



@router.get("/{idUsuario}")
async def obtener(idUsuario: str, usuario=Depends(usuario_actual)):
    if usuario.get("sub") != idUsuario and usuario.get("rol") != "admin":
        raise HTTPException(status_code=403, detail="No autorizado")
    return await service.listar_por_usuario(idUsuario)

