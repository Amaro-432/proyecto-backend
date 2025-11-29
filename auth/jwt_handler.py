import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException

SECRET_KEY = "clave-super-secreta"
ALGORITHM = "HS256"

def crear_token(data: dict):
    to_encode = data.copy()
    # ⚠️ convertir exp a timestamp entero
    expire = datetime.utcnow() + timedelta(hours=3)
    to_encode["exp"] = int(expire.timestamp())
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")
