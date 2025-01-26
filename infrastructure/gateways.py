from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from application import interfaces
from domain import entities


class DishGateway(interfaces.DishSaver, interfaces.DishReader, interfaces.DishRemover):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def read_all(self, owner: int) -> list[entities.DishDM]:
        query = text("SELECT * FROM dishes WHERE owner = :owner ORDER BY dish_type")
        result = await self._session.execute(statement=query, params={"owner": owner})
        rows = result.fetchall()
        return [
            entities.DishDM(
                uuid=row.uuid,
                name=row.name,
                random_weight=row.random_weight,
                dish_type=row.dish_type,
                owner=row.owner,
            )
            for row in rows
        ]

    async def read_all_by_dish_type(
        self, dish_type: str, owner: int, offset: int = 0, limit: int = 5
    ) -> list[entities.DishDM]:
        query = text(
            """
            SELECT * FROM dishes
            WHERE dish_type = :dish_type AND owner = :owner
            ORDER BY name
            OFFSET :offset LIMIT :limit
        """
        )
        result = await self._session.execute(
            statement=query,
            params={
                "dish_type": dish_type,
                "owner": owner,
                "offset": offset,
                "limit": limit,
            },
        )
        rows = result.fetchall()
        return [
            entities.DishDM(
                uuid=row.uuid,
                name=row.name,
                random_weight=row.random_weight,
                dish_type=row.dish_type,
                owner=row.owner,
            )
            for row in rows
        ]

    async def read_by_uuid(self, uuid: str, owner: int) -> entities.DishDM | None:
        query = text("SELECT * FROM dishes WHERE uuid = :uuid AND owner = :owner")
        result = await self._session.execute(
            statement=query,
            params={"uuid": uuid, "owner": owner},
        )
        row = result.fetchone()
        if not row:
            return None
        return entities.DishDM(
            uuid=row.uuid,
            name=row.name,
            dish_type=row.dish_type,
            random_weight=row.random_weight,
            owner=row.owner,
        )

    async def save(self, dish: entities.DishDM) -> None:
        query = text(
            "INSERT INTO dishes (uuid, name, random_weight, dish_type, owner) "
            "VALUES (:uuid, :name, :random_weight, :dish_type, :owner)"
        )
        await self._session.execute(
            statement=query,
            params={
                "uuid": dish.uuid,
                "name": dish.name,
                "random_weight": dish.random_weight,
                "dish_type": dish.dish_type,
                "owner": dish.owner,
            },
        )

    async def remove_by_uuid(self, uuid: str, owner: int) -> None:
        query = text("DELETE FROM dishes WHERE uuid=:uuid AND owner = :owner")
        await self._session.execute(
            statement=query,
            params={
                "uuid": uuid,
                "owner": owner,
            },
        )
        await self._session.commit()
