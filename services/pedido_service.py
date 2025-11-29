from models.pedido import Pedido
from repositories.pedido_repo import PedidoRepository
from repositories.carrito_repo import CarritoRepository
from config import db
from pymongo import ReturnDocument   # 👈 necesario para find_one_and_update

repo = PedidoRepository()
carrito_repo = CarritoRepository(db)

# --- Función para obtener el siguiente número de pedido ---
async def get_next_pedido_number():
    counter = await db["counters"].find_one_and_update(
        {"_id": "pedido"},
        {"$inc": {"seq": 1}},   # incrementa en 1
        upsert=True,            # si no existe, lo crea
        return_document=ReturnDocument.AFTER
    )
    return counter["seq"]

# --- Listar pedidos por usuario ---
async def listar_por_usuario(idUsuario: str):
    pedidos_cursor = await repo.query({"idUsuario": idUsuario})
    pedidos = []
    async for p in pedidos_cursor:
        p["id"] = str(p["_id"])
        del p["_id"]
        pedidos.append(p)
    return pedidos

# --- Confirmar pedido ---
async def confirmar(idUsuario: str, total: float):
    carrito = await carrito_repo.find_by_user(idUsuario)

    # Obtener número secuencial
    numeroPedido = await get_next_pedido_number()

    # Enriquecer items con subtotal
    items = []
    for it in carrito.get("items", []):
        subtotal = it["precio"] * it["cantidad"]
        items.append({
            **it,
            "subtotal": subtotal
        })

    pedido = Pedido(
        idUsuario=idUsuario,
        total=total,
        items=items,
        numeroPedido=str(numeroPedido)   # 👈 ahora es 110, 111, etc.
    ).dict()

    idPedido = await repo.create(pedido)

    # Vaciar carrito luego de comprar
    await carrito_repo.col.update_one(
        {"user_id": idUsuario},
        {"$set": {"items": []}}
    )

    return {
        "idPedido": str(idPedido),
        "numeroPedido": numeroPedido,
        "estado": "confirmado"
    }
