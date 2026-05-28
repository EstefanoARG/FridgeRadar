
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.inventario import InventarioCreate, InventarioResponse, InventarioUpdate
from app.services.inventario_service import InventarioService

router = APIRouter()


@router.get("/hogar/{id_hogar}", response_model=list[InventarioResponse])
async def listar_inventario(
    id_hogar: int,
    estado: str | None = Query(None, description="verde | amarillo | rojo | vencido"),
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = InventarioService(db)
    return await service.listar(id_hogar=id_hogar, estado=estado)


@router.post("/hogar/{id_hogar}", response_model=InventarioResponse, status_code=status.HTTP_201_CREATED)
async def agregar_producto(
    id_hogar: int,
    data: InventarioCreate,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = InventarioService(db)
    return await service.agregar(id_hogar=id_hogar, data=data, id_usuario=current_user)


@router.get("/{id_inventario}", response_model=InventarioResponse)
async def obtener_item(
    id_inventario: int,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = InventarioService(db)
    return await service.obtener(id_inventario)


@router.patch("/{id_inventario}", response_model=InventarioResponse)
async def actualizar_item(
    id_inventario: int,
    data: InventarioUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = InventarioService(db)
    return await service.actualizar(
        id_inventario=id_inventario, data=data, id_usuario=current_user
    )


@router.delete("/{id_inventario}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_item(
    id_inventario: int,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = InventarioService(db)
    await service.eliminar(id_inventario=id_inventario, id_usuario=current_user)
