from fastapi import APIRouter, UploadFile, File, Query
from models.producto import Producto
from services import producto_service as service
import shutil
import uuid
import os

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.post("/")
async def crear(producto: Producto):
    return await service.crear_producto(producto)

@router.get("/")
async def listar(
    categoria: str | None = Query(None),
    precio_min: float | None = Query(None),
    precio_max: float | None = Query(None)
):
    return await service.listar_productos(categoria, precio_min, precio_max)

@router.get("/{id}")
async def obtener(id: str):
    return await service.obtener_producto(id)

@router.put("/{id}")
async def actualizar(id: str, producto: Producto):
    return await service.actualizar_producto(id, producto)

@router.delete("/{id}")
async def eliminar(id: str):
    return await service.eliminar_producto(id)

@router.post("/upload-image")
async def subir_imagen(file: UploadFile = File(...)):
    extension = file.filename.split(".")[-1]
    nombre_archivo = f"{uuid.uuid4()}.{extension}"

    ruta = f"static/{nombre_archivo}"

    with open(ruta, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"url": f"/static/{nombre_archivo}"}


