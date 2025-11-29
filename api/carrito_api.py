from fastapi import APIRouter, Depends
from services import carrito_service as service
from auth.dependencies import usuario_actual

router = APIRouter(prefix="/carrito", tags=["Carrito"])

@router.get("/")
async def obtener_carrito(usuario=Depends(usuario_actual)):
    return await service.obtener(usuario["sub"])

@router.post("/add")
async def add(idProducto: str, cantidad: int, usuario=Depends(usuario_actual)):
    return await service.agregar(usuario["sub"], idProducto, cantidad)

@router.post("/remove")
async def remove(idProducto: str, usuario=Depends(usuario_actual)):
    return await service.eliminar(usuario["sub"], idProducto)
