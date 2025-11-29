from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class BoletaItem(BaseModel):
    idProducto: str
    nombre: str
    cantidad: int
    precio: float
    subtotal: float

class Boleta(BaseModel):
    idUsuario: str
    idPedido: str
    numeroPedido: str | None = None
    fecha: datetime = Field(default_factory=datetime.utcnow)
    items: List[BoletaItem]
    subtotal: float
    estado: str = "emitida"

