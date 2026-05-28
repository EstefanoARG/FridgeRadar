from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import NotFoundError
from app.models.lista_compra import ListaCompra
from app.models.lista_compra_detalle import ListaCompraDetalle
from app.schemas.lista_compra import (
    ListaCompraCreate,
    ListaCompraDetalleCreate,
    ListaCompraDetalleResponse,
    ListaCompraDetalleUpdate,
    ListaCompraResponse,
    ListaCompraUpdate,
)


class ListaCompraService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def crear(self, data: ListaCompraCreate, id_usuario: int | None = None) -> ListaCompraResponse:
        lista = ListaCompra(
            id_hogar=data.id_hogar,
            nombre=data.nombre,
        )
        self.db.add(lista)
        await self.db.flush()

        for item_data in data.items:
            detalle = ListaCompraDetalle(
                id_lista=lista.id_lista,
                id_producto=item_data.id_producto,
                cantidad=item_data.cantidad,
                unidad=item_data.unidad,
                prioridad=item_data.prioridad,
                nota=item_data.nota,
            )
            self.db.add(detalle)

        await self.db.flush()
        return await self._cargar_con_detalles(lista.id_lista)

    async def obtener(self, id_lista: int) -> ListaCompraResponse:
        return await self._cargar_con_detalles(id_lista)

    async def listar_por_hogar(self, id_hogar: int) -> list[ListaCompraResponse]:
        stmt = (
            select(ListaCompra)
            .where(ListaCompra.id_hogar == id_hogar)
            .order_by(ListaCompra.fecha_creacion.desc())
            .options(selectinload(ListaCompra.detalles))
        )
        result = await self.db.execute(stmt)
        listas = result.scalars().all()
        return [self._to_response(l) for l in listas]

    async def actualizar(
        self, id_lista: int, data: ListaCompraUpdate
    ) -> ListaCompraResponse:
        lista = await self.db.get(ListaCompra, id_lista)
        if not lista:
            raise NotFoundError("Lista de compra no encontrada")

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None:
                setattr(lista, key, value)
        await self.db.flush()
        return await self._cargar_con_detalles(id_lista)

    async def eliminar(self, id_lista: int) -> None:
        lista = await self.db.get(ListaCompra, id_lista)
        if not lista:
            raise NotFoundError("Lista de compra no encontrada")

        await self.db.execute(
            delete(ListaCompraDetalle).where(ListaCompraDetalle.id_lista == id_lista)
        )
        await self.db.delete(lista)
        await self.db.flush()

    async def agregar_detalle(
        self, id_lista: int, data: ListaCompraDetalleCreate
    ) -> ListaCompraResponse:
        lista = await self.db.get(ListaCompra, id_lista)
        if not lista:
            raise NotFoundError("Lista de compra no encontrada")

        detalle = ListaCompraDetalle(
            id_lista=id_lista,
            id_producto=data.id_producto,
            cantidad=data.cantidad,
            unidad=data.unidad,
            prioridad=data.prioridad,
            nota=data.nota,
        )
        self.db.add(detalle)
        await self.db.flush()
        return await self._cargar_con_detalles(id_lista)

    async def actualizar_detalle(
        self, id_detalle: int, data: ListaCompraDetalleUpdate
    ) -> ListaCompraResponse:
        detalle = await self.db.get(ListaCompraDetalle, id_detalle)
        if not detalle:
            raise NotFoundError("Detalle de lista no encontrado")

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None:
                setattr(detalle, key, value)
        await self.db.flush()
        return await self._cargar_con_detalles(detalle.id_lista)

    async def eliminar_detalle(self, id_detalle: int) -> ListaCompraResponse:
        detalle = await self.db.get(ListaCompraDetalle, id_detalle)
        if not detalle:
            raise NotFoundError("Detalle de lista no encontrado")

        id_lista = detalle.id_lista
        await self.db.delete(detalle)
        await self.db.flush()
        return await self._cargar_con_detalles(id_lista)

    async def marcar_comprado(self, id_detalle: int) -> ListaCompraResponse:
        detalle = await self.db.get(ListaCompraDetalle, id_detalle)
        if not detalle:
            raise NotFoundError("Detalle de lista no encontrado")

        detalle.comprado = not detalle.comprado
        await self.db.flush()
        return await self._cargar_con_detalles(detalle.id_lista)

    async def agregar_item(self, id_lista: int, data: ListaCompraDetalleCreate) -> ListaCompraDetalleResponse:
        """Alias for agregar_detalle but returns the detalle response instead."""
        lista = await self.db.get(ListaCompra, id_lista)
        if not lista:
            raise NotFoundError("Lista de compra no encontrada")

        detalle = ListaCompraDetalle(
            id_lista=id_lista,
            id_producto=data.id_producto,
            cantidad=data.cantidad,
            unidad=data.unidad,
            prioridad=data.prioridad,
            nota=data.nota,
        )
        self.db.add(detalle)
        await self.db.flush()
        await self.db.refresh(detalle)
        return ListaCompraDetalleResponse.model_validate(detalle)

    async def actualizar_item(self, id_detalle: int, data: ListaCompraDetalleUpdate) -> ListaCompraDetalleResponse:
        """Alias for actualizar_detalle but returns the detalle response instead."""
        detalle = await self.db.get(ListaCompraDetalle, id_detalle)
        if not detalle:
            raise NotFoundError("Detalle de lista no encontrado")

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None:
                setattr(detalle, key, value)
        await self.db.flush()
        await self.db.refresh(detalle)
        return ListaCompraDetalleResponse.model_validate(detalle)

    async def eliminar_item(self, id_detalle: int) -> None:
        """Alias for eliminar_detalle but returns None like the endpoint expects."""
        detalle = await self.db.get(ListaCompraDetalle, id_detalle)
        if not detalle:
            raise NotFoundError("Detalle de lista no encontrado")

        await self.db.delete(detalle)
        await self.db.flush()

    async def _cargar_con_detalles(self, id_lista: int) -> ListaCompraResponse:
        stmt = (
            select(ListaCompra)
            .where(ListaCompra.id_lista == id_lista)
            .options(selectinload(ListaCompra.detalles))
        )
        result = await self.db.execute(stmt)
        lista = result.scalar_one_or_none()
        if not lista:
            raise NotFoundError("Lista de compra no encontrada")
        return self._to_response(lista)

    def _to_response(self, lista: ListaCompra) -> ListaCompraResponse:
        response = ListaCompraResponse.model_validate(lista)
        response.items = [
            ListaCompraDetalleResponse.model_validate(d) for d in lista.detalles
        ]
        return response
