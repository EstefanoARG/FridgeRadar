import math

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.inventario import Inventario
from app.models.receta import Receta
from app.models.sugerencia import SugerenciaReceta
from app.schemas.sugerencia import SugerenciaResponse
from app.utils.semaforo import AMARILLO, ROJO

ESTADOS_CRITICOS = {AMARILLO, ROJO}


class TengoHambreService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def sugerir(
        self, id_hogar: int, solo_criticos: bool, limite: int, id_usuario: int
    ) -> list[SugerenciaResponse]:
        recetas_stmt = (
            select(Receta)
            .where(Receta.es_publica == True)
            .options(selectinload(Receta.ingredientes))
        )
        result = await self.db.execute(recetas_stmt)
        recetas = result.scalars().all()

        inventario_stmt = select(Inventario).where(Inventario.id_hogar == id_hogar)
        inv_result = await self.db.execute(inventario_stmt)
        items_inventario = inv_result.scalars().all()

        inventario_por_producto: dict[int, list[Inventario]] = {}
        for item in items_inventario:
            inventario_por_producto.setdefault(item.id_producto, []).append(item)

        sugerencias: list[tuple[float, bool, Receta]] = []

        for receta in recetas:
            if not receta.ingredientes:
                continue

            total = len(receta.ingredientes)
            encontrados = 0
            usa_criticos = False

            for ing in receta.ingredientes:
                inv_items = inventario_por_producto.get(ing.id_producto, [])
                if not inv_items:
                    continue

                if solo_criticos:
                    items_criticos = [
                        i for i in inv_items if i.estado_caducidad in ESTADOS_CRITICOS
                    ]
                    if items_criticos:
                        encontrados += 1
                        usa_criticos = True
                else:
                    encontrados += 1
                    if any(i.estado_caducidad in ESTADOS_CRITICOS for i in inv_items):
                        usa_criticos = True

            porcentaje = (encontrados / total) * 100
            porcentaje = math.floor(porcentaje * 100) / 100

            if porcentaje >= 70.0:
                sugerencias.append((porcentaje, usa_criticos, receta))

        sugerencias.sort(key=lambda x: (-x[1], -x[0]))
        sugerencias = sugerencias[:limite]

        select_stmt = select(SugerenciaReceta).where(
            SugerenciaReceta.id_usuario == id_usuario,
            SugerenciaReceta.id_hogar == id_hogar,
        )
        old = await self.db.execute(select_stmt)
        for old_sug in old.scalars().all():
            await self.db.delete(old_sug)
        await self.db.flush()

        responses = []
        for porcentaje, usa_criticos, receta in sugerencias:
            sug = SugerenciaReceta(
                id_usuario=id_usuario,
                id_hogar=id_hogar,
                id_receta=receta.id_receta,
                porcentaje_coincidencia=porcentaje,
                usa_productos_criticos=usa_criticos,
            )
            self.db.add(sug)
            await self.db.flush()

            responses.append(
                SugerenciaResponse(
                    id_receta=receta.id_receta,
                    nombre=receta.nombre,
                    descripcion=receta.descripcion,
                    tiempo_preparacion=receta.tiempo_preparacion,
                    dificultad=receta.dificultad,
                    porciones=receta.porciones,
                    imagen=receta.imagen,
                    calorias=receta.calorias,
                    porcentaje_match=porcentaje,
                    usa_criticos=usa_criticos,
                )
            )

        return responses
