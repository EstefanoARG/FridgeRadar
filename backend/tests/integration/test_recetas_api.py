import pytest


@pytest.mark.asyncio
async def test_listar_recetas_publicas(client):
    response = await client.get("/api/v1/recetas/")
    assert response.status_code in (200, 401)
