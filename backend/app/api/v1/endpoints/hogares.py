
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.hogar import (
    HogarCreate,
    HogarResponse,
    HogarUpdate,
    UsuarioHogarCreate,
    UsuarioHogarResponse,
)
from app.services.hogar_service import HogarService

router = APIRouter()


@router.post("/", response_model=HogarResponse, status_code=status.HTTP_201_CREATED)
async def crear_hogar(
    data: HogarCreate,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = HogarService(db)
    return await service.crear(data, id_usuario=current_user)


@router.get("/", response_model=list[HogarResponse])
async def listar_mis_hogares(
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = HogarService(db)
    return await service.listar_por_usuario(current_user)


@router.get("/{id_hogar}", response_model=HogarResponse)
async def obtener_hogar(
    id_hogar: int,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = HogarService(db)
    return await service.obtener(id_hogar)


@router.patch("/{id_hogar}", response_model=HogarResponse)
async def actualizar_hogar(
    id_hogar: int,
    data: HogarUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = HogarService(db)
    return await service.actualizar(id_hogar, data, id_usuario=current_user)


@router.delete("/{id_hogar}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_hogar(
    id_hogar: int,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = HogarService(db)
    await service.eliminar(id_hogar, id_usuario=current_user)


@router.post("/{id_hogar}/miembros", response_model=UsuarioHogarResponse, status_code=status.HTTP_201_CREATED)
async def agregar_miembro(
    id_hogar: int,
    data: UsuarioHogarCreate,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = HogarService(db)
    return await service.agregar_miembro(id_hogar, data, id_usuario=current_user)


@router.get("/{id_hogar}/miembros", response_model=list[UsuarioHogarResponse])
async def listar_miembros(
    id_hogar: int,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = HogarService(db)
    return await service.listar_miembros(id_hogar)


@router.delete("/{id_hogar}/miembros/{id_usuario_hogar}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_miembro(
    id_hogar: int,
    id_usuario_hogar: int,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = HogarService(db)
    await service.remover_miembro(id_hogar, id_usuario_hogar, id_usuario=current_user)
