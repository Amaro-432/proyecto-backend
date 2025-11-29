from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.usuario_api import router as usuario_router
from api.producto_api import router as producto_router
from api.carrito_api import router as carrito_router
from api.pedido_api import router as pedido_router
from api.pago_api import router as pago_router
from api.despacho_api import router as despacho_router
from api.auth_api import router as auth_router
from fastapi.staticfiles import StaticFiles



app = FastAPI(title="Queso & Sabor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # ← Permitir todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],        # ← Permitir todos los métodos (GET, POST, PUT, DELETE)
    allow_headers=["*"],        # ← Permitir cualquier encabezado
)

app.mount("/static", StaticFiles(directory="static"), name="static")



app.include_router(usuario_router)
app.include_router(producto_router)
app.include_router(carrito_router)
app.include_router(pedido_router)
app.include_router(pago_router)
app.include_router(despacho_router)
app.include_router(auth_router)


@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Queso & Sabor"}




