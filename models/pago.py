from pydantic import BaseModel
from typing import Optional

class Pago(BaseModel):
    idUsuario: str
    idPedido: str
    monto: float
    metodo: str       # ("efectivo", "transferencia", "webpay")
    estado: str = "pendiente"
    token: Optional[str] = None 
