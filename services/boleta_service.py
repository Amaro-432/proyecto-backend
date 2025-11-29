from repositories.boleta_repo import BoletaRepository
from datetime import datetime, timedelta
from repositories.usuario_repo import UsuarioRepository
from repositories.producto_repo import ProductoRepository
from collections import defaultdict


boleta_repo = BoletaRepository()
usuario_repo= UsuarioRepository()
producto_repo=ProductoRepository()

async def ranking_productos():
    cursor = boleta_repo.collection.find({"estado": "emitida"})
    boletas = await cursor.to_list(length=None)

    ranking = {}
    for b in boletas:
        for item in b["items"]:
            nombre = item["nombre"]
            if nombre not in ranking:
                ranking[nombre] = {"ventas": 0, "monto": 0}
            ranking[nombre]["ventas"] += item["cantidad"]
            ranking[nombre]["monto"] += item["subtotal"]

    resultado = [
        {"producto": k, "ventas": v["ventas"], "monto": v["monto"]}
        for k, v in ranking.items()
    ]
    resultado.sort(key=lambda x: x["ventas"], reverse=True)
    return resultado

async def resumen_por_periodo(desde: str, hasta: str):
    # Convertir strings a datetime
    desde_dt = datetime.fromisoformat(desde)
    # incluir todo el día hasta las 23:59
    hasta_dt = datetime.fromisoformat(hasta) + timedelta(days=1)

    cursor = boleta_repo.collection.find({
        "fecha": {"$gte": desde_dt, "$lt": hasta_dt},
        "estado": "emitida"
    })
    boletas = await cursor.to_list(length=None)

    total_monto = sum(b["total"] for b in boletas)
    promedio = round(total_monto / len(boletas), 2) if boletas else 0
    return {
        "cantidad": len(boletas),
        "monto": total_monto,
        "promedio": promedio
    }



async def detalle_filtrado(idProducto: str, correo_cliente: str, desde: str, hasta: str):
    desde_dt = datetime.fromisoformat(desde)
    hasta_dt = datetime.fromisoformat(hasta) + timedelta(days=1)

    usuario = await usuario_repo.find_by_email(correo_cliente)
    if not usuario:
        print("Usuario no encontrado:", correo_cliente)
        return []

    # Convertir ObjectId a string para que coincida con boleta.idUsuario
    idUsuario = str(usuario["_id"])

    cursor = boleta_repo.collection.find({
        "fecha": {"$gte": desde_dt, "$lt": hasta_dt},
        "idUsuario": idUsuario,
        "estado": "emitida",
        "items.idProducto": idProducto
    })
    boletas = await cursor.to_list(length=None)


    detalle = []
    for b in boletas:
        for item in b["items"]:
            if item["idProducto"] == idProducto:
                detalle.append({
                    "producto": item["nombre"],
                    "cliente": correo_cliente,
                    "fecha": b["fecha"],
                    "cantidad": item["cantidad"],
                    "total": item["subtotal"]
                })
    return detalle

async def evolucion_ventas(dt_desde: datetime, dt_hasta: datetime):
    cursor = boleta_repo.collection.find({
        "estado": "emitida",
        "fecha": {"$gte": dt_desde, "$lte": dt_hasta}
    })
    boletas = await cursor.to_list(length=None)

    agrupado = defaultdict(lambda: {"monto_total": 0, "cantidad_pedidos": 0})

    for b in boletas:
        fecha = b["fecha"]
        clave_mes = fecha.strftime("%Y-%m")
        agrupado[clave_mes]["monto_total"] += b.get("total", 0)
        agrupado[clave_mes]["cantidad_pedidos"] += 1

    resultado = []
    for mes in sorted(agrupado.keys()):
        datos = agrupado[mes]
        promedio = round(datos["monto_total"] / datos["cantidad_pedidos"], 2) if datos["cantidad_pedidos"] else 0
        resultado.append({
            "mes": mes,
            "monto_total": datos["monto_total"],
            "cantidad_pedidos": datos["cantidad_pedidos"],
            "promedio_por_pedido": promedio
        })

    return resultado


