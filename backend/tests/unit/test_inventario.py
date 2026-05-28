import pytest

from app.models.categoria_producto import CategoriaProducto
from app.models.estante import Estante
from app.models.hogar import Hogar
from app.models.producto import Producto
from app.models.usuario import Usuario
from app.models.zona import Zona
from app.schemas.inventario import InventarioCreate
from app.services.inventario_service import InventarioService


@pytest.mark.asyncio
async def test_agregar_producto(db):
    usuario = Usuario(nombres="Test", correo="test@test.com", password_hash="hash")
    hogar = Hogar(nombre="Test Hogar")
    categoria = CategoriaProducto(nombre="Test Cat")
    db.add_all([usuario, hogar, categoria])
    await db.flush()

    producto = Producto(nombre="Test Producto", id_categoria=categoria.id_categoria)
    zona = Zona(id_hogar=hogar.id_hogar, nombre="Test Zona", tipo="refrigerador")
    db.add_all([producto, zona])
    await db.flush()

    estante = Estante(id_zona=zona.id_zona, nombre="Test Estante", posicion_vertical=1)
    db.add(estante)
    await db.flush()

    service = InventarioService(db)
    data = InventarioCreate(
        id_producto=producto.id_producto,
        id_estante=estante.id_estante,
        cantidad=2.0,
    )
    result = await service.agregar(
        id_hogar=hogar.id_hogar, data=data, id_usuario=usuario.id_usuario
    )
    assert result.cantidad == 2.0
    assert result.id_hogar == hogar.id_hogar
