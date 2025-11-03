from pydantic import BaseModel
from datetime import datetime

class Pedido(BaseModel):
    id: str | None = None
    idUsuario: str
    fecha: datetime = datetime.utcnow()
    estado: str = "pendiente"
    total: float
