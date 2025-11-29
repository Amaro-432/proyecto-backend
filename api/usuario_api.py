from fastapi import APIRouter, Depends, HTTPException
from models.usuario import Usuario, EmailUpdate
from models.perfil import Perfil 
from services.usuario_service import (
    registrar, login, obtener_perfil, actualizar_perfil,
    listar_usuarios, actualizar_usuario, eliminar_usuario
)
from auth.dependencies import solo_admin, usuario_actual
from repositories.usuario_repo import UsuarioRepository
from pydantic import EmailStr

repo = UsuarioRepository()


    
router = APIRouter(prefix="/usuario", tags=["Usuario"])

@router.post("/registro")
async def registro(usuario: Usuario):
    return await registrar(usuario)

@router.post("/login")
async def iniciar_sesion(correo: str, password: str):
    return await login(correo, password)

@router.get("/perfil/{idUsuario}")
async def get_perfil(idUsuario: str):
    return await obtener_perfil(idUsuario)

@router.put("/perfil/{idUsuario}")
async def put_perfil(idUsuario: str, perfil: Perfil):
    return await actualizar_perfil(idUsuario, perfil)

# --- Sección de administración ---
@router.get("/", dependencies=[Depends(solo_admin)])
async def get_usuarios():
    return await listar_usuarios()

@router.put("/{idUsuario}", dependencies=[Depends(solo_admin)])
async def put_usuario(idUsuario: str, data: dict):
    return await actualizar_usuario(idUsuario, data)

@router.delete("/{idUsuario}", dependencies=[Depends(solo_admin)])
async def delete_usuario(idUsuario: str):
    return await eliminar_usuario(idUsuario)

@router.get("/by-email/{correo}", dependencies=[Depends(solo_admin)])
async def get_usuario_por_correo(correo: str):
    usuario = await repo.find_by_email(correo)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario["_id"] = str(usuario["_id"])
    if "password" in usuario:
        del usuario["password"]
    return usuario

@router.put("/{idUsuario}/rol", dependencies=[Depends(solo_admin)])
async def actualizar_rol(idUsuario: str, nuevo_rol: dict):
    if "rol" not in nuevo_rol:
        raise HTTPException(status_code=400, detail="Falta campo 'rol'")
    return await repo.update(idUsuario, {"rol": nuevo_rol["rol"]})

@router.put("/{idUsuario}/correo")
async def actualizar_correo(
    idUsuario: str,
    nuevo: EmailUpdate,
    usuario = Depends(usuario_actual)
):
    if usuario.get("sub") != idUsuario:
        raise HTTPException(status_code=403, detail="No puedes cambiar el correo de otro usuario")

    nuevo_email = nuevo.email

    existente = await repo.find_by_email(nuevo_email)
    if existente:
        raise HTTPException(status_code=409, detail="Correo ya registrado")

    actualizado = await repo.update(idUsuario, {"email": nuevo_email})
    if not actualizado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {"status": "ok", "msg": "Correo actualizado correctamente"}


