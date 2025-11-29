from pydantic import BaseModel

class Perfil(BaseModel):
    id: str | None = None
    nombre: str
    telefono: str | None = None
    direccion: str | None = None
    comuna: str | None = None
    
    
