from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class PedidoItem(BaseModel):
    idProducto: str
    nombre: str
    cantidad: int
    precio: float
    subtotal: float

class Pedido(BaseModel):
    id: str | None = None
    idUsuario: str
    fecha: datetime = Field(default_factory=datetime.utcnow)
    estado: str = "pendiente"
    total: float
    items: List[PedidoItem] = []
    numeroPedido: str | None = None
