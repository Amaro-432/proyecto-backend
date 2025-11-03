from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "clave-super-secreta"
ALGORITHM = "HS256"

def crear_token(data: dict):
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + timedelta(hours=3)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
