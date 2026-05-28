from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginationParams(BaseModel):
    page:     int = 1
    per_page: int = 20

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.per_page


class PagedResponse(BaseModel, Generic[T]):
    items:    list[T]
    total:    int
    page:     int
    per_page: int
    pages:    int
