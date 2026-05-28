from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.inventario import Inventario
from app.models.movimiento_inventario import MovimientoInventario
from app.schemas.inventario import (
    InventarioCreate,
    InventarioResponse,
    InventarioUpdate,
    MovimientoInventarioResponse,
)


class InventarioService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def listar(
        self, id_hogar: int, estado: str | None = None
    ) -> list[InventarioResponse]:
        stmt = (
            select(Inventario)
            .where(Inventario.id_hogar == id_hogar)
            .order_by(Inventario.fecha_registro.desc())
        )
        if estado:
            stmt = stmt.where(Inventario.estado_caducidad == estado)
        result = await self.db.execute(stmt)
        items = result.scalars().all()
        return [InventarioResponse.model_validate(i) for i in items]

    async def agregar(
        self, id_hogar: int, data: InventarioCreate, id_usuario: int
    ) -> InventarioResponse:
        inventario = Inventario(
            id_hogar=id_hogar,
            id_producto=data.id_producto,
            id_estante=data.id_estante,
            id_usuario_agrego=id_usuario,
            cantidad=data.cantidad,
            fecha_compra=data.fecha_compra,
            fecha_vencimiento=data.fecha_vencimiento,
            abierto=data.abierto,
            observaciones=data.observaciones,
        )
        self.db.add(inventario)
        await self.db.flush()
        await self.db.refresh(inventario)

        movimiento = MovimientoInventario(
            id_inventario=inventario.id_inventario,
            id_usuario=id_usuario,
            tipo_movimiento="agregado",
            cantidad=data.cantidad,
            descripcion="Producto agregado al inventario",
        )
        self.db.add(movimiento)
        await self.db.flush()

        return InventarioResponse.model_validate(inventario)

    async def obtener(self, id_inventario: int) -> InventarioResponse:
        inventario = await self.db.get(Inventario, id_inventario)
        if not inventario:
            raise NotFoundError("Item de inventario no encontrado")
        return InventarioResponse.model_validate(inventario)

    async def actualizar(
        self, id_inventario: int, data: InventarioUpdate, id_usuario: int
    ) -> InventarioResponse:
        inventario = await self.db.get(Inventario, id_inventario)
        if not inventario:
            raise NotFoundError("Item de inventario no encontrado")

        update_data = data.model_dump(exclude_unset=True)
        cambios = []
        for key, value in update_data.items():
            if value is not None:
                old_val = getattr(inventario, key, None)
                if old_val != value:
                    setattr(inventario, key, value)
                    cambios.append(f"{key}: {old_val} -> {value}")

        if cambios:
            await self.db.flush()
            await self.db.refresh(inventario)
            movimiento = MovimientoInventario(
                id_inventario=id_inventario,
                id_usuario=id_usuario,
                tipo_movimiento="movido",
                descripcion="; ".join(cambios),
            )
            self.db.add(movimiento)
            await self.db.flush()

        return InventarioResponse.model_validate(inventario)

    async def eliminar(self, id_inventario: int, id_usuario: int) -> None:
        inventario = await self.db.get(Inventario, id_inventario)
        if not inventario:
            raise NotFoundError("Item de inventario no encontrado")

        movimiento = MovimientoInventario(
            id_inventario=id_inventario,
            id_usuario=id_usuario,
            tipo_movimiento="eliminado",
            descripcion="Producto eliminado del inventario",
        )
        self.db.add(movimiento)
        await self.db.flush()

        await self.db.delete(inventario)
        await self.db.flush()

    async def obtener_movimientos(
        self, id_inventario: int
    ) -> list[MovimientoInventarioResponse]:
        inventario = await self.db.get(Inventario, id_inventario)
        if not inventario:
            raise NotFoundError("Item de inventario no encontrado")

        stmt = (
            select(MovimientoInventario)
            .where(MovimientoInventario.id_inventario == id_inventario)
            .order_by(MovimientoInventario.fecha_movimiento.desc())
        )
        result = await self.db.execute(stmt)
        movimientos = result.scalars().all()
        return [MovimientoInventarioResponse.model_validate(m) for m in movimientos]
