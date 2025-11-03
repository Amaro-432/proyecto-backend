from pydantic import BaseModel, EmailStr
from models.perfil import Perfil

class Usuario(BaseModel):
    id: str | None = None
    nombre: str
    correo: EmailStr
    passw: str
    perfil: str  # solo guardamos el nombre del perfil
    rol: str   # "cliente", "admin", "dueno", "despacho"
