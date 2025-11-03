from models.pedido import Pedido
from repositories.pedido_repo import PedidoRepository
from repositories.carrito_repo import CarritoRepository

repo = PedidoRepository()
carrito_repo = CarritoRepository()

async def confirmar(idUsuario: str, total: float):
    carrito = await carrito_repo.obtener(idUsuario)

    pedido = Pedido(idUsuario=idUsuario, total=total).dict()
    idPedido = await repo.create(pedido)

    # vaciar carrito luego de comprar
    await carrito_repo.actualizar(idUsuario, {"idUsuario": idUsuario, "items": []})

    return {"pedido": idPedido, "estado": "confirmado"}

async def listar_por_usuario(idUsuario: str):
    pedidos = await repo.query({"idUsuario": idUsuario})
    return [p async for p in pedidos]

