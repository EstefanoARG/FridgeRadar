from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.hogar import Hogar
from app.models.usuario_hogar import UsuarioHogar


class HogarRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, nombre: str, codigo_invitacion: str | None = None) -> Hogar:
        hogar = Hogar(nombre=nombre, codigo_invitacion=codigo_invitacion)
        self.db.add(hogar)
        await self.db.flush()
        await self.db.refresh(hogar)
        return hogar

    async def get_by_id(self, id_hogar: int) -> Hogar | None:
        result = await self.db.execute(
            select(Hogar).where(Hogar.id_hogar == id_hogar)
        )
        return result.scalar_one_or_none()

    async def get_by_codigo_invitacion(self, codigo: str) -> Hogar | None:
        result = await self.db.execute(
            select(Hogar).where(Hogar.codigo_invitacion == codigo)
        )
        return result.scalar_one_or_none()

    async def list_all(self) -> list[Hogar]:
        result = await self.db.execute(select(Hogar))
        return result.scalars().all()

    async def list_by_usuario(self, id_usuario: int) -> list[Hogar]:
        stmt = (
            select(Hogar)
            .join(UsuarioHogar, UsuarioHogar.id_hogar == Hogar.id_hogar)
            .where(UsuarioHogar.id_usuario == id_usuario)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update(self, id_hogar: int, **kwargs) -> Hogar | None:
        hogar = await self.get_by_id(id_hogar)
        if hogar is None:
            return None
        for key, value in kwargs.items():
            if value is not None:
                setattr(hogar, key, value)
        await self.db.flush()
        await self.db.refresh(hogar)
        return hogar

    async def delete(self, id_hogar: int) -> bool:
        hogar = await self.get_by_id(id_hogar)
        if hogar is None:
            return False
        await self.db.delete(hogar)
        await self.db.flush()
        return True

    async def add_miembro(
        self,
        id_usuario: int,
        id_hogar: int,
        rol: str = "miembro",
    ) -> UsuarioHogar:
        usuario_hogar = UsuarioHogar(
            id_usuario=id_usuario,
            id_hogar=id_hogar,
            rol=rol,
        )
        self.db.add(usuario_hogar)
        await self.db.flush()
        await self.db.refresh(usuario_hogar)
        return usuario_hogar

    async def get_miembros(self, id_hogar: int) -> list[UsuarioHogar]:
        result = await self.db.execute(
            select(UsuarioHogar).where(UsuarioHogar.id_hogar == id_hogar)
        )
        return result.scalars().all()

    async def get_miembro(self, id_usuario_hogar: int) -> UsuarioHogar | None:
        result = await self.db.execute(
            select(UsuarioHogar).where(
                UsuarioHogar.id_usuario_hogar == id_usuario_hogar
            )
        )
        return result.scalar_one_or_none()

    async def remove_miembro(self, id_usuario_hogar: int) -> bool:
        usuario_hogar = await self.get_miembro(id_usuario_hogar)
        if usuario_hogar is None:
            return False
        await self.db.delete(usuario_hogar)
        await self.db.flush()
        return True
