from fastapi import APIRouter, Query, Request, HTTPException, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from pydantic import BaseModel
from models.pago import Pago
from models.boleta import BoletaItem
from services import pago_service as service, webpay_service
from services import boleta_service
from repositories.pedido_repo import pedido_repo
from repositories.pago_repo import pago_repo
from repositories.boleta_repo import BoletaRepository
from typing import List, Optional
from datetime import datetime, timedelta
import json



router = APIRouter(prefix="/pago", tags=["Pago & Boleta"])


boleta_repo = BoletaRepository()
class PagoRequest(BaseModel):
    pago: Pago
    items: List[BoletaItem]
    

@router.post("/iniciar")
async def iniciar_pago(request: PagoRequest, req: Request):
    # URL de retorno hacia /pago/confirmar
    base_url = str(req.base_url).rstrip("/")
    return_url = f"{base_url}/pago/confirmar"

    token, url = await webpay_service.iniciar_transaccion(
        request.pago.idPedido,
        request.pago.monto,
        return_url
    )

    # Guardar token en el pago
    request.pago.token = token
    await pago_repo.crear(request.pago.dict())

    return {"token": token, "url": url}


@router.post("/procesar")
async def procesar(request: PagoRequest):
    return await service.procesar_pago(request.pago, request.items)





@router.api_route("/confirmar", methods=["GET", "POST"])
async def confirmar_pago(request: Request, token_ws: str = Form(None)):
    # obtener token desde GET o POST
    if token_ws is None:
        token_ws = request.query_params.get("token_ws")

    if token_ws is None:
        raise HTTPException(400, "token_ws no recibido")

    result = await webpay_service.confirmar_transaccion(token_ws)

    if result["status"] != "AUTHORIZED":
        raise HTTPException(400, "Pago no autorizado")

    pago_db = await pago_repo.find_by_token(token_ws)
    if not pago_db:
        raise HTTPException(404, "Pago no encontrado")

    pago = Pago(**pago_db)

    pedido = await pedido_repo.get(pago.idPedido)
    items = [BoletaItem(**item) for item in pedido["items"]]

    # Aquí se crea la boleta
    boleta = await service.procesar_pago(pago, items)

    # en /confirmar (FastAPI)
    html = f"""
    <script>
        // idBoleta viene del resultado de procesar_pago()
        const id = "{boleta["id"]}";
        // redirige al frontend incluyendo el id en querystring
        window.location.href = "http://127.0.0.1:5501/boleta.html?boletaId=" + encodeURIComponent(id);
    </script>
    """
    return HTMLResponse(content=html)

@router.get("/boleta/{idBoleta}")
async def obtener_boleta(idBoleta: str):
    boleta = await boleta_repo.obtener(idBoleta)
    if not boleta:
        raise HTTPException(status_code=404, detail="Boleta no encontrada")
    return boleta

@router.get("/ranking")
async def obtener_ranking():
    return await boleta_service.ranking_productos()

@router.get("/reporte/resumen")
async def obtener_resumen(
    desde: str = Query(..., description="Fecha de inicio en formato YYYY-MM-DD"),
    hasta: str = Query(..., description="Fecha de fin en formato YYYY-MM-DD")
):
    return await boleta_service.resumen_por_periodo(desde, hasta)

@router.get("/reporte/detalle")
async def obtener_detalle(producto: str, cliente: str, desde: str, hasta: str):
    # producto ya es el id
    return await boleta_service.detalle_filtrado(producto, cliente, desde, hasta)


@router.get("/reporte/evolucion")
async def obtener_evolucion(
    desde: Optional[str] = Query(None, description="Fecha inicio YYYY-MM-DD"),
    hasta: Optional[str] = Query(None, description="Fecha fin YYYY-MM-DD")
):
    hoy = datetime.utcnow()
    inicio_mes_actual = hoy.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    inicio_mes_anterior = (inicio_mes_actual - timedelta(days=1)).replace(day=1)

    def parse_fecha(s: Optional[str], default: datetime) -> datetime:
        if not s:
            return default
        # Acepta YYYY-MM-DD y añade hora UTC
        try:
            return datetime.fromisoformat(s)
        except ValueError:
            # Fallback: "YYYY-MM-DD"
            try:
                return datetime.strptime(s, "%Y-%m-%d")
            except ValueError:
                return default

    dt_desde = parse_fecha(desde, inicio_mes_anterior)
    dt_hasta = parse_fecha(hasta, hoy)

    return await boleta_service.evolucion_ventas(dt_desde, dt_hasta)

