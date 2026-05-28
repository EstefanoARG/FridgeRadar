
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.usuario import UsuarioResponse, UsuarioUpdate
from app.services.usuario_service import UsuarioService

router = APIRouter()


@router.get("/me", response_model=UsuarioResponse)
async def obtener_perfil(
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = UsuarioService(db)
    return await service.obtener_perfil(current_user)


@router.patch("/me", response_model=UsuarioResponse)
async def actualizar_perfil(
    data: UsuarioUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = UsuarioService(db)
    return await service.actualizar_perfil(current_user, data)


@router.get("/", response_model=list[UsuarioResponse])
async def listar_usuarios(
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = UsuarioService(db)
    return await service.listar_usuarios()
