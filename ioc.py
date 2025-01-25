from typing import AsyncIterable
from uuid import uuid4

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from dishka import Provider, Scope, provide, AnyOf, from_context
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from application import interfaces
from application.interactors import (
    GetDishInteractor,
    NewDishInteractor,
    GetAllDishInteractor,
    GenerateMenuInteractor,
    GetAllDishByTypeInteractor,
    DeleteDishInteractor,
)
from config import Config
from infrastructure.database import new_session_maker
from infrastructure.gateways import DishGateway


class AppProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_uuid_generator(self) -> interfaces.UUIDGenerator:
        return uuid4

    @provide(scope=Scope.APP)
    def get_session_maker(self, config: Config) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config.postgres)

    @provide(scope=Scope.APP)
    def get_bot(self, config: Config) -> Bot:
        return Bot(
            token=config.bot.token, default=DefaultBotProperties(parse_mode="HTML")
        )

    @provide(scope=Scope.APP)
    def get_dispatcher(self, bot: Bot) -> Dispatcher:
        return Dispatcher(bot=bot)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[
        AnyOf[
            AsyncSession,
            interfaces.DBSession,
        ]
    ]:
        async with session_maker() as session:
            yield session

    dish_gateway = provide(
        DishGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[
            interfaces.DishReader, interfaces.DishSaver, interfaces.DishRemover
        ],
    )

    get_dish_interactor = provide(GetDishInteractor, scope=Scope.REQUEST)
    get_all_dish_interactor = provide(GetAllDishInteractor, scope=Scope.REQUEST)
    get_all_dish_by_type_interactor = provide(
        GetAllDishByTypeInteractor, scope=Scope.REQUEST
    )
    create_new_dish_interactor = provide(NewDishInteractor, scope=Scope.REQUEST)
    delete_dish_interactor = provide(DeleteDishInteractor, scope=Scope.REQUEST)
    generate_menu_interactor = provide(GenerateMenuInteractor, scope=Scope.REQUEST)
