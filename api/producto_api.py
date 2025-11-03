from fastapi import APIRouter
from models.producto import Producto
from services import producto_service as service

router = APIRouter(prefix="/producto", tags=["Producto"])

@router.post("/")
async def nuevo(producto: Producto):
    return await service.agregar(producto)

@router.get("/")
async def obtener():
    return await service.listar()

@router.put("/{id}")
async def modificar(id: str, producto: Producto):
    return await service.actualizar(id, producto)

@router.delete("/{id}")
async def borrar(id: str):
    return await service.eliminar(id)

