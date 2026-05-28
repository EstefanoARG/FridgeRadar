from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.categoria_producto import CategoriaProducto
from app.models.producto import Producto


class ProductoRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, nombre: str, **kwargs) -> Producto:
        producto = Producto(nombre=nombre, **kwargs)
        self.db.add(producto)
        await self.db.flush()
        await self.db.refresh(producto)
        return producto

    async def get_by_id(self, id_producto: int) -> Producto | None:
        result = await self.db.execute(
            select(Producto).where(Producto.id_producto == id_producto)
        )
        return result.scalar_one_or_none()

    async def get_by_codigo_barras(self, codigo_barras: str) -> Producto | None:
        result = await self.db.execute(
            select(Producto).where(Producto.codigo_barras == codigo_barras)
        )
        return result.scalar_one_or_none()

    async def search_by_nombre(self, nombre: str) -> list[Producto]:
        result = await self.db.execute(
            select(Producto).where(Producto.nombre.ilike(f"%{nombre}%"))
        )
        return result.scalars().all()

    async def list_all(self) -> list[Producto]:
        result = await self.db.execute(select(Producto))
        return result.scalars().all()

    async def list_by_categoria(self, id_categoria: int) -> list[Producto]:
        result = await self.db.execute(
            select(Producto).where(Producto.id_categoria == id_categoria)
        )
        return result.scalars().all()

    async def update(self, id_producto: int, **kwargs) -> Producto | None:
        producto = await self.get_by_id(id_producto)
        if producto is None:
            return None
        for key, value in kwargs.items():
            if value is not None:
                setattr(producto, key, value)
        await self.db.flush()
        await self.db.refresh(producto)
        return producto

    async def delete(self, id_producto: int) -> bool:
        producto = await self.get_by_id(id_producto)
        if producto is None:
            return False
        await self.db.delete(producto)
        await self.db.flush()
        return True

    async def create_categoria(
        self, nombre: str, icono: str | None = None, color: str | None = None
    ) -> CategoriaProducto:
        cat = CategoriaProducto(nombre=nombre, icono=icono, color=color)
        self.db.add(cat)
        await self.db.flush()
        await self.db.refresh(cat)
        return cat

    async def get_categoria_by_id(self, id_categoria: int) -> CategoriaProducto | None:
        result = await self.db.execute(
            select(CategoriaProducto).where(
                CategoriaProducto.id_categoria == id_categoria
            )
        )
        return result.scalar_one_or_none()

    async def list_categorias(self) -> list[CategoriaProducto]:
        result = await self.db.execute(select(CategoriaProducto))
        return result.scalars().all()

    async def update_categoria(
        self, id_categoria: int, **kwargs
    ) -> CategoriaProducto | None:
        cat = await self.get_categoria_by_id(id_categoria)
        if cat is None:
            return None
        for key, value in kwargs.items():
            if value is not None:
                setattr(cat, key, value)
        await self.db.flush()
        await self.db.refresh(cat)
        return cat

    async def delete_categoria(self, id_categoria: int) -> bool:
        cat = await self.get_categoria_by_id(id_categoria)
        if cat is None:
            return False
        await self.db.delete(cat)
        await self.db.flush()
        return True
