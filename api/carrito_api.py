from fastapi import APIRouter
from services import carrito_service as service

router = APIRouter(prefix="/carrito", tags=["Carrito"])

@router.post("/{idUsuario}/add")
async def add(idUsuario: str, idProducto: str, cantidad: int):
    return await service.agregar(idUsuario, idProducto, cantidad)

@router.post("/{idUsuario}/remove")
async def remove(idUsuario: str, idProducto: str):
    return await service.eliminar(idUsuario, idProducto)
