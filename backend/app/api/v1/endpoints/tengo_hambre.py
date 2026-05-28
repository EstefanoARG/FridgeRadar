
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.sugerencia import SugerenciaResponse
from app.services.tengo_hambre_service import TengoHambreService

router = APIRouter()


@router.get("/{id_hogar}", response_model=list[SugerenciaResponse])
async def tengo_hambre(
    id_hogar: int,
    solo_criticos: bool = Query(True,  description="Solo usa productos en amarillo/rojo"),
    limite:        int  = Query(10,    description="Máximo de recetas a devolver"),
    db: AsyncSession   = Depends(get_db),
    current_user: int  = Depends(get_current_user),
):
    """
    Devuelve recetas que puedes cocinar con lo que está a punto de vencer.
    Prioriza ingredientes en rojo y amarillo.
    """
    service = TengoHambreService(db)
    return await service.sugerir(
        id_hogar=id_hogar,
        solo_criticos=solo_criticos,
        limite=limite,
        id_usuario=current_user,
    )
