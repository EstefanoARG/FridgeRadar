import pytest

from app.schemas.usuario import UsuarioCreate
from app.services.auth_service import AuthService


@pytest.mark.asyncio
async def test_register_user(db):
    service = AuthService(db)
    data = UsuarioCreate(
        nombres="Test",
        apellidos="User",
        correo="test@example.com",
        password="secret123",
    )
    result = await service.registrar(data)
    assert result.nombres == "Test"
    assert result.correo == "test@example.com"
    assert result.id_usuario is not None


@pytest.mark.asyncio
async def test_register_duplicate_email(db):
    service = AuthService(db)
    data = UsuarioCreate(
        nombres="Test",
        correo="dupe@example.com",
        password="secret123",
    )
    await service.registrar(data)
    with pytest.raises(Exception):
        await service.registrar(data)


@pytest.mark.asyncio
async def test_login_success(db):
    service = AuthService(db)
    data = UsuarioCreate(
        nombres="Login",
        correo="login@example.com",
        password="mypassword",
    )
    await service.registrar(data)
    token = await service.login(correo="login@example.com", password="mypassword")
    assert token.access_token is not None
    assert token.token_type == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(db):
    service = AuthService(db)
    with pytest.raises(Exception):
        await service.login(correo="noexiste@test.com", password="wrong")
