import pytest

from app.services.tengo_hambre_service import TengoHambreService


@pytest.mark.asyncio
async def test_sugerir_sin_inventario(db):
    service = TengoHambreService(db)
    result = await service.sugerir(
        id_hogar=999,
        solo_criticos=True,
        limite=5,
        id_usuario=1,
    )
    assert result == []
