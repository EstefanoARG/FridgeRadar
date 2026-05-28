from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.repositories.producto_repository import ProductoRepository
from app.schemas.producto import (
    CategoriaProductoCreate,
    CategoriaProductoResponse,
    ProductoConCategoriaResponse,
    ProductoCreate,
    ProductoResponse,
    ProductoUpdate,
)


class ProductoService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = ProductoRepository(db)

    async def crear(self, data: ProductoCreate) -> ProductoResponse:
        producto = await self.repo.create(
            nombre=data.nombre,
            descripcion=data.descripcion,
            id_categoria=data.id_categoria,
            codigo_barras=data.codigo_barras,
            unidad_medida=data.unidad_medida,
            perecible=data.perecible,
            dias_promedio_vencimiento=data.dias_promedio_vencimiento,
            imagen=data.imagen,
        )
        return ProductoResponse.model_validate(producto)

    async def listar(
        self, q: str | None = None, id_categoria: int | None = None
    ) -> list[ProductoResponse]:
        if q:
            productos = await self.repo.search_by_nombre(q)
        elif id_categoria is not None:
            productos = await self.repo.list_by_categoria(id_categoria)
        else:
            productos = await self.repo.list_all()
        return [ProductoResponse.model_validate(p) for p in productos]

    async def obtener(self, id_producto: int) -> ProductoConCategoriaResponse:
        producto = await self.repo.get_by_id(id_producto)
        if not producto:
            raise NotFoundError("Producto no encontrado")
        categoria = None
        if producto.categoria:
            categoria = CategoriaProductoResponse.model_validate(producto.categoria)
        response = ProductoConCategoriaResponse.model_validate(producto)
        response.categoria = categoria
        return response

    async def actualizar(self, id_producto: int, data: ProductoUpdate) -> ProductoResponse:
        update_data = data.model_dump(exclude_unset=True)
        producto = await self.repo.update(id_producto, **update_data)
        if not producto:
            raise NotFoundError("Producto no encontrado")
        return ProductoResponse.model_validate(producto)

    async def eliminar(self, id_producto: int) -> None:
        deleted = await self.repo.delete(id_producto)
        if not deleted:
            raise NotFoundError("Producto no encontrado")

    async def crear_categoria(self, data: CategoriaProductoCreate) -> CategoriaProductoResponse:
        cat = await self.repo.create_categoria(
            nombre=data.nombre,
            icono=data.icono,
            color=data.color,
        )
        return CategoriaProductoResponse.model_validate(cat)

    async def listar_categorias(self) -> list[CategoriaProductoResponse]:
        categorias = await self.repo.list_categorias()
        return [CategoriaProductoResponse.model_validate(c) for c in categorias]
