from repositories.pedido_repo import PedidoRepository
from repositories.boleta_repo import BoletaRepository
from repositories.pago_repo import PagoRepository
from services import despacho_service, usuario_service
from models.despacho import Despacho
from models.pago import Pago
from models.boleta import Boleta, BoletaItem
from models.pedido import Pedido
from fastapi import HTTPException
from typing import List
from config import db

pedido_repo = PedidoRepository()
boleta_repo = BoletaRepository()
pago_repo = PagoRepository()

async def procesar_pago(pago: Pago, items: List[BoletaItem] = None):

    idPago = await pago_repo.crear(pago.dict())
    await pago_repo.confirmar(idPago)

    # SIEMPRE: obtener pedido
    pedido = await pedido_repo.get(pago.idPedido)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    # Si no vienen items, tomarlos desde el pedido
    if not items or len(items) == 0:
        items = [BoletaItem(**item) for item in pedido["items"]]

    # Calcular totales
    subtotal = sum(item.subtotal for item in items)
    iva = round(subtotal * 0.19, 2)
    total = subtotal + iva

    # Crear boleta incluyendo numeroPedido
    boleta = Boleta(
        idUsuario=pago.idUsuario,
        idPedido=pago.idPedido,
        numeroPedido=pedido["numeroPedido"],   # 👈 YA NO FALLA
        items=items,
        subtotal=subtotal,
        iva=iva,
        total=total
    )

    boleta_id = await boleta_repo.crear(boleta.model_dump())

    # Crear despacho
    perfil_cliente = await usuario_service.obtener_perfil(pago.idUsuario)
    direccion_cliente = perfil_cliente.get("direccion") if perfil_cliente else None

    despacho = Despacho(
        idPedido=pago.idPedido,
        direccion=direccion_cliente or "SIN DIRECCION",
        encargado="",
        estado="pendiente"
    )

    idDespacho = await despacho_service.asignar_despacho(despacho)

    return {
        "id": str(boleta_id["id"]),
        "estado": "pago confirmado",
        "idPago": str(idPago),
        "idPedido": pago.idPedido,
        "numeroPedido": pedido["numeroPedido"],   # 👈 OPCIONAL EN RESPUESTA
        "idUsuario": pago.idUsuario,
        "idDespacho": str(idDespacho["idDespacho"]),
        "subtotal": subtotal,
        "iva": iva,
        "total": total,
        "items": [item.model_dump() for item in items]
    }


    
    

    
    

