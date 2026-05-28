from fastapi import APIRouter

from app.api.v1.endpoints import (
    alertas,
    auth,
    desperdicio,
    hogares,
    inventario,
    listas_compra,
    productos,
    recetas,
    semaforo,
    tengo_hambre,
    usuarios,
    zonas,
)

api_router = APIRouter()

api_router.include_router(auth.router,          prefix="/auth",          tags=["Auth"])
api_router.include_router(usuarios.router,      prefix="/usuarios",      tags=["Usuarios"])
api_router.include_router(hogares.router,       prefix="/hogares",       tags=["Hogares"])
api_router.include_router(zonas.router,         prefix="/zonas",         tags=["Zonas"])
api_router.include_router(inventario.router,    prefix="/inventario",    tags=["Inventario"])
api_router.include_router(productos.router,     prefix="/productos",     tags=["Productos"])
api_router.include_router(recetas.router,       prefix="/recetas",       tags=["Recetas"])
api_router.include_router(alertas.router,       prefix="/alertas",       tags=["Alertas"])
api_router.include_router(listas_compra.router, prefix="/listas-compra", tags=["Listas de Compra"])
api_router.include_router(desperdicio.router,   prefix="/desperdicio",   tags=["Desperdicio"])
api_router.include_router(semaforo.router,      prefix="/semaforo",      tags=["Semáforo"])
api_router.include_router(tengo_hambre.router,  prefix="/tengo-hambre",  tags=["Tengo Hambre"])
