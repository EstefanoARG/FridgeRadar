import pytest


@pytest.mark.asyncio
async def test_alertas_no_leidas(client):
    response = await client.get("/api/v1/alertas/contar")
    assert response.status_code in (200, 401)
