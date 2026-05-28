
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.lista_compra import (
    ListaCompraCreate,
    ListaCompraDetalleCreate,
    ListaCompraDetalleResponse,
    ListaCompraDetalleUpdate,
    ListaCompraResponse,
    ListaCompraUpdate,
)
from app.services.lista_compra_service import ListaCompraService

router = APIRouter()


@router.post("/", response_model=ListaCompraResponse, status_code=status.HTTP_201_CREATED)
async def crear_lista(
    data: ListaCompraCreate,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = ListaCompraService(db)
    return await service.crear(data, id_usuario=current_user)


@router.get("/", response_model=list[ListaCompraResponse])
async def listar_por_hogar(
    id_hogar: int = Query(..., description="ID del hogar"),
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = ListaCompraService(db)
    return await service.listar_por_hogar(id_hogar)


@router.get("/{id_lista}", response_model=ListaCompraResponse)
async def obtener_lista(
    id_lista: int,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = ListaCompraService(db)
    return await service.obtener(id_lista)


@router.patch("/{id_lista}", response_model=ListaCompraResponse)
async def actualizar_lista(
    id_lista: int,
    data: ListaCompraUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = ListaCompraService(db)
    return await service.actualizar(id_lista, data)


@router.delete("/{id_lista}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_lista(
    id_lista: int,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = ListaCompraService(db)
    await service.eliminar(id_lista)


@router.post("/{id_lista}/items", response_model=ListaCompraDetalleResponse, status_code=status.HTTP_201_CREATED)
async def agregar_item(
    id_lista: int,
    data: ListaCompraDetalleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = ListaCompraService(db)
    return await service.agregar_item(id_lista, data)


@router.patch("/items/{id_detalle}", response_model=ListaCompraDetalleResponse)
async def actualizar_item(
    id_detalle: int,
    data: ListaCompraDetalleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = ListaCompraService(db)
    return await service.actualizar_item(id_detalle, data)


@router.delete("/items/{id_detalle}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_item(
    id_detalle: int,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = ListaCompraService(db)
    await service.eliminar_item(id_detalle)
