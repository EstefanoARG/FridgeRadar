
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.desperdicio import DesperdicioCreate, DesperdicioResponse
from app.services.desperdicio_service import DesperdicioService

router = APIRouter()


@router.post("/", response_model=DesperdicioResponse, status_code=status.HTTP_201_CREATED)
async def registrar_desperdicio(
    data: DesperdicioCreate,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = DesperdicioService(db)
    return await service.registrar(data, id_usuario=current_user)


@router.get("/", response_model=list[DesperdicioResponse])
async def listar_por_hogar(
    id_hogar: int = Query(..., description="ID del hogar"),
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = DesperdicioService(db)
    return await service.listar_por_hogar(id_hogar)


@router.get("/metricas/{id_hogar}")
async def obtener_metricas(
    id_hogar: int,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = DesperdicioService(db)
    return await service.obtener_metricas(id_hogar)
