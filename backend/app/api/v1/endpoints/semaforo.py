from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.services.semaforo_service import SemaforoService

router = APIRouter()


@router.post("/recalcular")
async def recalcular_todos(
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = SemaforoService(db)
    resultados = await service.recalcular_todos()
    return {"message": "Semáforos recalculados", "total_actualizados": resultados}


@router.post("/recalcular/{id_hogar}")
async def recalcular_por_hogar(
    id_hogar: int,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = SemaforoService(db)
    resultados = await service.recalcular_por_hogar(id_hogar)
    return {"message": f"Semáforos recalculados para hogar {id_hogar}", "actualizados": resultados}
