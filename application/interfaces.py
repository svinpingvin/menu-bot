from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from domain import entities


class DishSaver(Protocol):
    @abstractmethod
    async def save(self, dish: entities.DishDM) -> None: ...


class DishRemover(Protocol):
    @abstractmethod
    async def remove_by_uuid(self, uuid: str) -> None: ...


class DishReader(Protocol):
    @abstractmethod
    async def read_by_uuid(self, uuid: str) -> entities.DishDM | None: ...

    @abstractmethod
    async def read_all(self) -> list[entities.DishDM] | None: ...

    @abstractmethod
    async def read_all_by_dish_type(
        self, dish_type: str = None, offset: int = 0, limit: int = 5
    ) -> list[entities.DishDM] | None: ...


class UUIDGenerator(Protocol):
    def __call__(self) -> UUID: ...


class DBSession(Protocol):
    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def flush(self) -> None: ...
