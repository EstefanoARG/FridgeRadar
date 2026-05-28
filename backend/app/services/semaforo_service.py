from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.alerta import Alerta
from app.models.inventario import Inventario
from app.utils.semaforo import calcular_estado


class SemaforoService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def recalcular_todos(self) -> int:
        stmt = select(Inventario)
        result = await self.db.execute(stmt)
        items = result.scalars().all()

        actualizados = 0
        for item in items:
            nuevo_estado = calcular_estado(item.fecha_vencimiento)
            if item.estado_caducidad != nuevo_estado:
                item.estado_caducidad = nuevo_estado
                actualizados += 1

        if actualizados:
            await self.db.flush()

        return actualizados

    async def recalcular_por_hogar(self, id_hogar: int) -> int:
        stmt = select(Inventario).where(Inventario.id_hogar == id_hogar)
        result = await self.db.execute(stmt)
        items = result.scalars().all()

        actualizados = 0
        for item in items:
            nuevo_estado = calcular_estado(item.fecha_vencimiento)
            if item.estado_caducidad != nuevo_estado:
                item.estado_caducidad = nuevo_estado
                actualizados += 1

        if actualizados:
            await self.db.flush()

        return actualizados

    async def generar_alertas_vencimiento(self) -> int:
        stmt = select(Inventario).where(
            Inventario.estado_caducidad.in_(["rojo", "vencido"])
        )
        result = await self.db.execute(stmt)
        items = result.scalars().all()

        generadas = 0
        for item in items:
            if item.estado_caducidad == "vencido":
                titulo = "Producto vencido"
                mensaje = (
                    f"El producto venció hace {abs((item.fecha_vencimiento - date.today()).days)} días"
                    if item.fecha_vencimiento
                    else "Producto vencido"
                )
            else:
                dias = (item.fecha_vencimiento - date.today()).days if item.fecha_vencimiento else 0
                titulo = "Producto por vencer"
                mensaje = f"Quedan {dias} días para que venza el producto"

            if item.id_usuario_agrego:
                alerta = Alerta(
                    id_usuario=item.id_usuario_agrego,
                    id_inventario=item.id_inventario,
                    titulo=titulo,
                    mensaje=mensaje,
                    tipo="vencimiento",
                )
                self.db.add(alerta)
                generadas += 1

        if generadas:
            await self.db.flush()

        return generadas
