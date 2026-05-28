
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.zona import ZonaCreate, ZonaResponse, ZonaUpdate
from app.services.zona_service import ZonaService

router = APIRouter()


@router.post("/", response_model=ZonaResponse, status_code=status.HTTP_201_CREATED)
async def crear_zona(
    data: ZonaCreate,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = ZonaService(db)
    return await service.crear(data)


@router.get("/", response_model=list[ZonaResponse])
async def listar_zonas(
    id_hogar: int | None = Query(None, description="Filtrar por hogar"),
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = ZonaService(db)
    return await service.listar(id_hogar=id_hogar)


@router.get("/{id_zona}", response_model=ZonaResponse)
async def obtener_zona(
    id_zona: int,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = ZonaService(db)
    return await service.obtener(id_zona)


@router.patch("/{id_zona}", response_model=ZonaResponse)
async def actualizar_zona(
    id_zona: int,
    data: ZonaUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = ZonaService(db)
    return await service.actualizar(id_zona, data)


@router.delete("/{id_zona}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_zona(
    id_zona: int,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = ZonaService(db)
    await service.eliminar(id_zona)
