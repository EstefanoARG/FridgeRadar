from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.usuario import TokenResponse, UsuarioCreate, UsuarioResponse
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)
    return await service.login(
        correo=form_data.username,
        password=form_data.password,
    )


@router.post("/register", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def register(
    data: UsuarioCreate,
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)
    return await service.registrar(data)
