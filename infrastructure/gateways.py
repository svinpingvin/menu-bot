from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from application.interfaces import DishReader, DishSaver
from domain.entities import DishDM


class DishGateway(
    DishSaver,
    DishReader,
):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def read_all(self) -> list[DishDM]:
        query = text("SELECT * FROM dishes")
        result = await self._session.execute(query)
        rows = result.fetchall()
        return [
            DishDM(
                uuid=row.uuid,
                name=row.name,
                random_weight=row.random_weight,
            )
            for row in rows
        ]

    async def read_by_uuid(self, uuid: str) -> DishDM | None:
        query = text("SELECT * FROM dishes WHERE uuid = :uuid")
        result = await self._session.execute(
            statement=query,
            params={"uuid": uuid},
        )
        row = result.fetchone()
        if not row:
            return None
        return DishDM(
            uuid=row.uuid,
            name=row.name,
            random_weight=row.random_weight,
        )

    async def save(self, dish: DishDM) -> None:
        query = text(
            "INSERT INTO dishes (uuid, name, random_weight) VALUES (:uuid, :name, :random_weight)"
        )
        await self._session.execute(
            statement=query,
            params={
                "uuid": dish.uuid,
                "name": dish.name,
                "random_weight": dish.random_weight,
            },
        )
