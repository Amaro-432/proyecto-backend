from fastapi import APIRouter
from models.pago import Pago
from services import pago_service as service

router = APIRouter(prefix="/pago", tags=["Pago & Boleta"])

@router.post("/procesar")
async def procesar(pago: Pago):
    return await service.procesar_pago(pago)
