
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.receta import (
    RecetaCreate,
    RecetaDetalleResponse,
    RecetaResponse,
    RecetaUpdate,
    TagRecetaCreate,
    TagRecetaResponse,
)
from app.services.receta_service import RecetaService

router = APIRouter()


@router.post("/", response_model=RecetaDetalleResponse, status_code=status.HTTP_201_CREATED)
async def crear_receta(
    data: RecetaCreate,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = RecetaService(db)
    return await service.crear(data, id_usuario=current_user)


@router.get("/", response_model=list[RecetaResponse])
async def listar_recetas(
    q: str | None = Query(None, description="Búsqueda por nombre"),
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = RecetaService(db)
    return await service.listar_publicas(q=q)


@router.get("/{id_receta}", response_model=RecetaDetalleResponse)
async def obtener_receta(
    id_receta: int,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = RecetaService(db)
    return await service.obtener(id_receta)


@router.patch("/{id_receta}", response_model=RecetaDetalleResponse)
async def actualizar_receta(
    id_receta: int,
    data: RecetaUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = RecetaService(db)
    return await service.actualizar(id_receta, data, id_usuario=current_user)


@router.delete("/{id_receta}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_receta(
    id_receta: int,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = RecetaService(db)
    await service.eliminar(id_receta, id_usuario=current_user)


@router.post("/{id_receta}/favorito", status_code=status.HTTP_201_CREATED)
async def marcar_favorito(
    id_receta: int,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = RecetaService(db)
    await service.marcar_favorito(id_receta, id_usuario=current_user)


@router.delete("/{id_receta}/favorito", status_code=status.HTTP_204_NO_CONTENT)
async def quitar_favorito(
    id_receta: int,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = RecetaService(db)
    await service.quitar_favorito(id_receta, id_usuario=current_user)


@router.get("/favoritos/mios", response_model=list[RecetaResponse])
async def listar_favoritos(
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = RecetaService(db)
    return await service.listar_favoritos(id_usuario=current_user)


@router.post("/tags", response_model=TagRecetaResponse, status_code=status.HTTP_201_CREATED)
async def crear_tag(
    data: TagRecetaCreate,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = RecetaService(db)
    return await service.crear_tag(data)


@router.get("/tags", response_model=list[TagRecetaResponse])
async def listar_tags(
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = RecetaService(db)
    return await service.listar_tags()
