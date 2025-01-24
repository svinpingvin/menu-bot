from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from domain.entities import DishDM


class DishSaver(Protocol):
    @abstractmethod
    async def save(self, dish: DishDM) -> None: ...


class DishReader(Protocol):
    @abstractmethod
    async def read_by_uuid(self, uuid: str) -> DishDM | None: ...

    @abstractmethod
    async def read_all(self) -> list[DishDM] | None: ...


class UUIDGenerator(Protocol):
    def __call__(self) -> UUID: ...


class DBSession(Protocol):
    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def flush(self) -> None: ...
