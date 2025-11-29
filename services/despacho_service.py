from models.despacho import Despacho
from services import usuario_service
from repositories.despacho_repo import DespachoRepository
from repositories.pedido_repo import PedidoRepository
from repositories.usuario_repo import UsuarioRepository
from utils.mongo_helpers import serialize_doc
from bson import ObjectId


repo = DespachoRepository()
pedido_repo = PedidoRepository()
usuario_repo = UsuarioRepository()

async def asignar_despacho(despacho: Despacho):
    # Buscar encargados disponibles
    encargados = await usuario_service.listar_por_rol("edd")
    if not encargados:
        return {"status": "error", "msg": "No hay encargados de despacho disponibles"}

    # Por ahora asignamos el primero de la lista
    despacho.encargado = encargados[0]["_id"]

    idDespacho = await repo.crear(despacho.dict())
    return {"status": "ok", "idDespacho": idDespacho}

from models.despacho import Despacho
from services import usuario_service
from repositories.despacho_repo import DespachoRepository

repo = DespachoRepository()

async def asignar_despacho(despacho: Despacho):
    # Buscar encargados disponibles
    encargados = await usuario_service.listar_por_rol("edd")
    if not encargados:
        return {"status": "error", "msg": "No hay encargados de despacho disponibles"}

    # Por ahora asignamos el primero de la lista
    despacho.encargado = encargados[0]["_id"]

    idDespacho = await repo.crear(despacho.dict())
    return {"status": "ok", "idDespacho": idDespacho}

async def actualizar_estado(idDespacho: str, estado: str):
    return await repo.actualizar_estado(idDespacho, estado)

async def listar_por_estado(estado: str):
    cursor = repo.collection.find({"estado": estado})
    despachos = await cursor.to_list(length=None)

    # Serializar cada despacho
    for d in despachos:
        d["_id"] = str(d["_id"])
    return despachos

async def listar_historial():
    cursor = repo.collection.find({})
    despachos = await cursor.to_list(length=None)

    resultado = []
    for d in despachos:
        d["_id"] = str(d["_id"])

        # Buscar pedido asociado
        pedido = await pedido_repo.get(d["idPedido"])
        if pedido:
            pedido["_id"] = str(pedido["_id"])
            d["numeroPedido"] = pedido.get("numeroPedido")   # ✅ ahora correcto
            d["idUsuario"] = pedido.get("idUsuario")
            d["fecha"] = pedido.get("fecha")                 # ✅ fecha del pedido
            d["total"] = pedido.get("total")                 # ✅ total del pedido

            # Buscar cliente
            cliente = await usuario_repo.get(pedido["idUsuario"])
            if cliente:
                cliente["_id"] = str(cliente["_id"])
                d["clienteNombre"] = cliente.get("nombre")
        else:
            d["numeroPedido"] = "—"
            d["fecha"] = d.get("fecha") or ""
            d["total"] = 0
            d["clienteNombre"] = "—"
            

        resultado.append(d)

    return resultado




async def listar_por_encargado(idUsuario: str):
    cursor = repo.collection.find({"encargado": idUsuario})
    despachos = await cursor.to_list(length=None)

    resultado = []
    for d in despachos:
        d["_id"] = str(d["_id"])

        pedido = await pedido_repo.get(d["idPedido"])
        if pedido:
            pedido["_id"] = str(pedido["_id"])
            d["numeroPedido"] = pedido.get("numeroPedido")
            d["idUsuario"] = pedido.get("idUsuario")

            cliente = await usuario_repo.get(pedido["idUsuario"])
            if cliente:
                cliente["_id"] = str(cliente["_id"])
                d["clienteNombre"] = cliente.get("nombre")

        resultado.append(d)

    return resultado

async def obtener_detalle(idDespacho: str):
    despacho = await repo.collection.find_one({"_id": ObjectId(idDespacho)})
    if not despacho:
        return {"error": "DESPACHO_NO_ENCONTRADO"}

    despacho["_id"] = str(despacho["_id"])

    pedido = await pedido_repo.get(despacho["idPedido"])
    if not pedido:
        return {"error": "PEDIDO_NO_ENCONTRADO"}

    pedido["_id"] = str(pedido["_id"])
    cliente = await usuario_repo.get(pedido["idUsuario"])
    if not cliente:
        return {"error": "CLIENTE_NO_ENCONTRADO"}

    cliente["_id"] = str(cliente["_id"])

    return {
        "numeroPedido": pedido.get("numeroPedido"),
        "clienteNombre": cliente.get("nombre"),
        "direccion": despacho.get("direccion"),
        "estado": despacho.get("estado"),
        "productos": pedido.get("items", [])
    }
async def listar_por_cliente(idUsuario: str):
    # Buscar todos los despachos cuyo pedido pertenece al cliente
    cursor = repo.collection.find({})
    despachos = await cursor.to_list(length=None)

    resultado = []
    for d in despachos:
        d["_id"] = str(d["_id"])

        pedido = await pedido_repo.get(d["idPedido"])
        if pedido and pedido.get("idUsuario") == idUsuario:
            pedido["_id"] = str(pedido["_id"])
            d["numeroPedido"] = pedido.get("numeroPedido")
            d["productos"] = pedido.get("items", [])
            d["direccion"] = d.get("direccion")
            d["estado"] = d.get("estado")

            resultado.append(d)

    return resultado
async def actualizar_direccion(idDespacho: str, direccion: str):
    from bson import ObjectId
    result = await repo.collection.update_one(
        {"_id": ObjectId(idDespacho)},
        {"$set": {"direccion": direccion}}
    )
    if result.modified_count == 1:
        return {"status": "ok", "msg": "Dirección actualizada"}
    return {"status": "error", "msg": "No se pudo actualizar la dirección"}

async def anular_con_trazabilidad(idDespacho: str):
    despacho = await repo.collection.find_one({"_id": ObjectId(idDespacho)})
    if not despacho:
        return {"error": "DESPACHO_NO_ENCONTRADO"}

    idPedido = despacho.get("idPedido")

    # 🟥 Actualizar estado del despacho
    await repo.collection.update_one(
        {"_id": ObjectId(idDespacho)},
        {"$set": {"estado": "anulado"}}
    )

    # 🗑️ Eliminar pedido asociado
    if idPedido:
        await pedido_repo.collection.delete_one({"_id": ObjectId(idPedido)})

    return {"status": "ok", "msg": "Pedido eliminado y despacho marcado como anulado"}








