from pydantic import BaseModel


class Producto(BaseModel):
    nombre: str
    descripcion: str
    precio: float
    categoria: str
    stock: int
    imagen: str | None = None
    origen: str | None = None
    leche: str | None = None
    maduracion: str | None = None
    ideal: str | None = None
