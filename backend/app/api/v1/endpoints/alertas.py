
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.alerta import AlertaResponse
from app.services.alerta_service import AlertaService

router = APIRouter()


@router.get("/", response_model=list[AlertaResponse])
async def listar_alertas(
    solo_no_leidas: bool | None = Query(False, description="Solo alertas no leídas"),
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = AlertaService(db)
    return await service.listar(id_usuario=current_user, solo_no_leidas=solo_no_leidas)


@router.patch("/{id_alerta}", response_model=AlertaResponse)
async def marcar_leida(
    id_alerta: int,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = AlertaService(db)
    return await service.marcar_leida(id_alerta, id_usuario=current_user)


@router.get("/contar")
async def contar_no_leidas(
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = AlertaService(db)
    total = await service.contar_no_leidas(id_usuario=current_user)
    return {"no_leidas": total}


@router.get("/{id_alerta}", response_model=AlertaResponse)
async def obtener_alerta(
    id_alerta: int,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = AlertaService(db)
    return await service.obtener(id_alerta)


@router.delete("/{id_alerta}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_alerta(
    id_alerta: int,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = AlertaService(db)
    await service.eliminar(id_alerta, id_usuario=current_user)
