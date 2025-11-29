from fastapi import APIRouter
from models.despacho import Despacho
from services import despacho_service as service

router = APIRouter(prefix="/despacho", tags=["Despacho"])

# 1. Asignar despacho
@router.post("/asignar")
async def asignar(despacho: Despacho):
    return await service.asignar_despacho(despacho)

# 2. Actualizar estado 
@router.put("/estado/{idDespacho}")
async def actualizar(idDespacho: str, estado: str):
    return await service.actualizar_estado(idDespacho, estado)

# 3. Listar todos los despachos pendientes 
@router.get("/pendientes")
async def listar_pendientes():
    return await service.listar_por_estado("pendiente")

# 4. Confirmar despacho 
@router.put("/confirmar/{idDespacho}")
async def confirmar(idDespacho: str):
    return await service.actualizar_estado(idDespacho, "en preparacion")

@router.get("/historial")
async def historial():
    return await service.listar_historial()

@router.get("/encargado/{idUsuario}")
async def listar_por_encargado(idUsuario: str):
    return await service.listar_por_encargado(idUsuario)

@router.get("/detalle/{idDespacho}")
async def detalle(idDespacho: str):
    return await service.obtener_detalle(idDespacho)

@router.get("/cliente/{idUsuario}")
async def listar_por_cliente(idUsuario: str):
    return await service.listar_por_cliente(idUsuario)

@router.put("/direccion/{idDespacho}")
async def actualizar_direccion(idDespacho: str, direccion: str):
    return await service.actualizar_direccion(idDespacho, direccion)

@router.put("/anular/{idDespacho}")
async def anular_despacho(idDespacho: str):
    return await service.anular_con_trazabilidad(idDespacho)








