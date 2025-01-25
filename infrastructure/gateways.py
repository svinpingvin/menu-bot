from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from application.interfaces import DishReader, DishSaver, DishRemover
from domain.entities import DishDM


class DishGateway(DishSaver, DishReader, DishRemover):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def read_all(self) -> list[DishDM]:
        query = text("SELECT * FROM dishes ORDER BY dish_type")
        result = await self._session.execute(query)
        rows = result.fetchall()
        return [
            DishDM(
                uuid=row.uuid,
                name=row.name,
                random_weight=row.random_weight,
                dish_type=row.dish_type,
            )
            for row in rows
        ]

    async def read_all_by_dish_type(
        self, dish_type: str, offset: int = 0, limit: int = 5
    ) -> list[DishDM]:
        query = text(
            """
            SELECT * FROM dishes
            WHERE dish_type = :dish_type
            ORDER BY name
            OFFSET :offset LIMIT :limit
        """
        )
        result = await self._session.execute(
            query, {"dish_type": dish_type, "offset": offset, "limit": limit}
        )
        rows = result.fetchall()
        return [
            DishDM(
                uuid=row.uuid,
                name=row.name,
                random_weight=row.random_weight,
                dish_type=row.dish_type,
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
            "INSERT INTO dishes (uuid, name, random_weight, dish_type) VALUES (:uuid, :name, :random_weight, :dish_type)"
        )
        await self._session.execute(
            statement=query,
            params={
                "uuid": dish.uuid,
                "name": dish.name,
                "random_weight": dish.random_weight,
                "dish_type": dish.dish_type,
            },
        )

    async def remove_by_uuid(self, uuid: str) -> None:
        query = text("DELETE FROM dishes WHERE uuid=:uuid")
        await self._session.execute(
            statement=query,
            params={
                "uuid": uuid,
            },
        )
        await self._session.commit()
