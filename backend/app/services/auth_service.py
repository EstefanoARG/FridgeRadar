from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, NotFoundError
from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.usuario import TokenResponse, UsuarioCreate, UsuarioResponse


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = UsuarioRepository(db)

    async def registrar(self, data: UsuarioCreate) -> UsuarioResponse:
        existing = await self.repo.get_by_correo(data.correo)
        if existing:
            raise ConflictError("El correo ya está registrado")
        hashed = hash_password(data.password)
        usuario = await self.repo.create(
            nombres=data.nombres,
            apellidos=data.apellidos,
            correo=data.correo,
            password_hash=hashed,
        )
        return UsuarioResponse.model_validate(usuario)

    async def login(self, correo: str, password: str) -> TokenResponse:
        usuario = await self.repo.get_by_correo(correo)
        if not usuario or not verify_password(password, usuario.password_hash):
            raise NotFoundError("Credenciales inválidas")
        usuario.ultimo_acceso = datetime.utcnow()
        await self.db.flush()
        token = create_access_token({"sub": usuario.id_usuario})
        return TokenResponse(access_token=token)
