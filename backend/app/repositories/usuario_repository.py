from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.usuario import Usuario


class UsuarioRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self, nombres: str, apellidos: str | None, correo: str, password_hash: str
    ) -> Usuario:
        usuario = Usuario(
            nombres=nombres,
            apellidos=apellidos,
            correo=correo,
            password_hash=password_hash,
        )
        self.db.add(usuario)
        await self.db.flush()
        await self.db.refresh(usuario)
        return usuario

    async def get_by_id(self, id_usuario: int) -> Usuario | None:
        result = await self.db.execute(
            select(Usuario).where(Usuario.id_usuario == id_usuario)
        )
        return result.scalar_one_or_none()

    async def get_by_correo(self, correo: str) -> Usuario | None:
        result = await self.db.execute(
            select(Usuario).where(Usuario.correo == correo)
        )
        return result.scalar_one_or_none()

    async def list_all(self) -> list[Usuario]:
        result = await self.db.execute(select(Usuario))
        return result.scalars().all()

    async def update(
        self, id_usuario: int, **kwargs
    ) -> Usuario | None:
        usuario = await self.get_by_id(id_usuario)
        if usuario is None:
            return None
        for key, value in kwargs.items():
            if value is not None:
                setattr(usuario, key, value)
        await self.db.flush()
        await self.db.refresh(usuario)
        return usuario

    async def delete(self, id_usuario: int) -> bool:
        usuario = await self.get_by_id(id_usuario)
        if usuario is None:
            return False
        await self.db.delete(usuario)
        await self.db.flush()
        return True
