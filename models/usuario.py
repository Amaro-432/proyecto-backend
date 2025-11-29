from pydantic import BaseModel, EmailStr
from models.perfil import Perfil

class Usuario(BaseModel):
    nombre: str
    email: EmailStr
    password: str
    rol: str
    perfil: Perfil | None = None
class LoginRequest(BaseModel):
    email: str
    password: str

class EmailUpdate(BaseModel):
    email: EmailStr