from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.repositories.hogar_repository import HogarRepository
from app.schemas.hogar import (
    HogarCreate,
    HogarResponse,
    HogarUpdate,
    UsuarioHogarCreate,
    UsuarioHogarResponse,
)


class HogarService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = HogarRepository(db)

    async def crear(self, data: HogarCreate, id_usuario: int) -> HogarResponse:
        hogar = await self.repo.create(
            nombre=data.nombre,
            codigo_invitacion=data.codigo_invitacion,
        )
        await self.repo.add_miembro(
            id_usuario=id_usuario,
            id_hogar=hogar.id_hogar,
            rol="owner",
        )
        return HogarResponse.model_validate(hogar)

    async def listar_por_usuario(self, id_usuario: int) -> list[HogarResponse]:
        hogares = await self.repo.list_by_usuario(id_usuario)
        return [HogarResponse.model_validate(h) for h in hogares]

    async def obtener(self, id_hogar: int) -> HogarResponse:
        hogar = await self.repo.get_by_id(id_hogar)
        if not hogar:
            raise NotFoundError("Hogar no encontrado")
        return HogarResponse.model_validate(hogar)

    async def actualizar(self, id_hogar: int, data: HogarUpdate, id_usuario: int) -> HogarResponse:
        hogar = await self.repo.get_by_id(id_hogar)
        if not hogar:
            raise NotFoundError("Hogar no encontrado")
        hogar = await self.repo.update(id_hogar, nombre=data.nombre)
        if not hogar:
            raise NotFoundError("Hogar no encontrado")
        return HogarResponse.model_validate(hogar)

    async def eliminar(self, id_hogar: int, id_usuario: int) -> None:
        hogar = await self.repo.get_by_id(id_hogar)
        if not hogar:
            raise NotFoundError("Hogar no encontrado")
        await self.repo.delete(id_hogar)

    async def agregar_miembro(
        self, id_hogar: int, data: UsuarioHogarCreate, id_usuario: int
    ) -> UsuarioHogarResponse:
        hogar = await self.repo.get_by_id(id_hogar)
        if not hogar:
            raise NotFoundError("Hogar no encontrado")
        miembro = await self.repo.add_miembro(
            id_usuario=data.id_usuario,
            id_hogar=id_hogar,
            rol=data.rol,
        )
        return UsuarioHogarResponse.model_validate(miembro)

    async def listar_miembros(self, id_hogar: int) -> list[UsuarioHogarResponse]:
        hogar = await self.repo.get_by_id(id_hogar)
        if not hogar:
            raise NotFoundError("Hogar no encontrado")
        miembros = await self.repo.get_miembros(id_hogar)
        return [UsuarioHogarResponse.model_validate(m) for m in miembros]

    async def remover_miembro(
        self, id_hogar: int, id_usuario_hogar: int, id_usuario: int
    ) -> None:
        hogar = await self.repo.get_by_id(id_hogar)
        if not hogar:
            raise NotFoundError("Hogar no encontrado")
        miembro = await self.repo.get_miembro(id_usuario_hogar)
        if not miembro:
            raise NotFoundError("Miembro no encontrado")
        await self.repo.remove_miembro(id_usuario_hogar)
