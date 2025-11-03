from pydantic import BaseModel

class Producto(BaseModel):
    id: str | None = None
    nombre: str
    descripcion: str
    precio: float
    categoria: str
    stock: int
