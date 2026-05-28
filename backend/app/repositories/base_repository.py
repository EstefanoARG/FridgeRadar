from typing import Any, Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(
        self, db: AsyncSession, model_class: type[ModelType], pk_attr: str = "id"
    ):
        self.db = db
        self.model_class = model_class
        self.pk_attr = pk_attr

    def _get_pk(self, obj: ModelType) -> Any:
        return getattr(obj, self.pk_attr)

    async def create(self, **kwargs: Any) -> ModelType:
        obj = self.model_class(**kwargs)
        self.db.add(obj)
        await self.db.flush()
        await self.db.refresh(obj)
        return obj

    async def get_by_id(self, id: Any) -> ModelType | None:
        stmt = select(self.model_class).where(
            getattr(self.model_class, self.pk_attr) == id
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self) -> list[ModelType]:
        result = await self.db.execute(select(self.model_class))
        return result.scalars().all()

    async def update(self, id: Any, **kwargs: Any) -> ModelType | None:
        obj = await self.get_by_id(id)
        if obj is None:
            return None
        for key, value in kwargs.items():
            if value is not None:
                setattr(obj, key, value)
        await self.db.flush()
        await self.db.refresh(obj)
        return obj

    async def delete(self, id: Any) -> bool:
        obj = await self.get_by_id(id)
        if obj is None:
            return False
        await self.db.delete(obj)
        await self.db.flush()
        return True
