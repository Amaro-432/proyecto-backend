from pydantic import BaseModel

class Pago(BaseModel):
    idUsuario: str
    monto: float
    metodo: str       # ("efectivo", "transferencia", "webpay")
    estado: str = "pendiente"
