
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.producto import (
    CategoriaProductoCreate,
    CategoriaProductoResponse,
    ProductoConCategoriaResponse,
    ProductoCreate,
    ProductoResponse,
    ProductoUpdate,
)
from app.services.producto_service import ProductoService

router = APIRouter()


@router.post("/", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
async def crear_producto(
    data: ProductoCreate,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = ProductoService(db)
    return await service.crear(data)


@router.get("/", response_model=list[ProductoResponse])
async def listar_productos(
    q: str | None = Query(None, description="Búsqueda por nombre"),
    id_categoria: int | None = Query(None, description="Filtrar por categoría"),
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = ProductoService(db)
    return await service.listar(q=q, id_categoria=id_categoria)


@router.post("/categorias", response_model=CategoriaProductoResponse, status_code=status.HTTP_201_CREATED)
async def crear_categoria(
    data: CategoriaProductoCreate,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = ProductoService(db)
    return await service.crear_categoria(data)


@router.get("/categorias", response_model=list[CategoriaProductoResponse])
async def listar_categorias(
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = ProductoService(db)
    return await service.listar_categorias()


@router.get("/{id_producto}", response_model=ProductoConCategoriaResponse)
async def obtener_producto(
    id_producto: int,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = ProductoService(db)
    return await service.obtener(id_producto)


@router.patch("/{id_producto}", response_model=ProductoResponse)
async def actualizar_producto(
    id_producto: int,
    data: ProductoUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = ProductoService(db)
    return await service.actualizar(id_producto, data)


@router.delete("/{id_producto}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_producto(
    id_producto: int,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = ProductoService(db)
    await service.eliminar(id_producto)
