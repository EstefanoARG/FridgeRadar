import pytest


@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


@pytest.mark.asyncio
async def test_register_and_login(client):
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "nombres": "Test",
            "correo": "testapi@example.com",
            "password": "test123",
        },
    )
    assert response.status_code == 201

    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "testapi@example.com", "password": "test123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token is not None
