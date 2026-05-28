from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, NotFoundError
from app.core.security import hash_password
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.usuario import UsuarioResponse, UsuarioUpdate


class UsuarioService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = UsuarioRepository(db)

    async def obtener_perfil(self, id_usuario: int) -> UsuarioResponse:
        usuario = await self.repo.get_by_id(id_usuario)
        if not usuario:
            raise NotFoundError("Usuario no encontrado")
        return UsuarioResponse.model_validate(usuario)

    async def actualizar_perfil(
        self, id_usuario: int, data: UsuarioUpdate
    ) -> UsuarioResponse:
        usuario = await self.repo.get_by_id(id_usuario)
        if not usuario:
            raise NotFoundError("Usuario no encontrado")

        if data.correo is not None and data.correo != usuario.correo:
            existing = await self.repo.get_by_correo(data.correo)
            if existing:
                raise ConflictError("El correo ya está registrado por otro usuario")

        update_data = data.model_dump(exclude_unset=True)
        if "password" in update_data and update_data["password"] is not None:
            update_data["password_hash"] = hash_password(update_data.pop("password"))
        if "correo" in update_data and update_data["correo"] is None:
            update_data.pop("correo")

        usuario = await self.repo.update(id_usuario, **update_data)
        if not usuario:
            raise NotFoundError("Usuario no encontrado")
        return UsuarioResponse.model_validate(usuario)

    async def listar_usuarios(self) -> list[UsuarioResponse]:
        usuarios = await self.repo.list_all()
        return [UsuarioResponse.model_validate(u) for u in usuarios]
