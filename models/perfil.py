from pydantic import BaseModel

class Perfil(BaseModel):
    id: str | None = None
    nombre: str
    descripcion: str | None = None
