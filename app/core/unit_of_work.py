from abc import ABC, abstractmethod

from app.core.database import async_session_maker


class IUnitOfWork(ABC):
    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, *args):
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class UnitOfWork(IUnitOfWork):

    def __init__(self):
        self.session_maker = async_session_maker
        self.user = None
        self.category = None
        self.location = None

    async def __aenter__(self):
        self.session = self.session_maker()

        from app.modules.categories.repositories import CategoryRepository
        from app.modules.locations.repositories import LocationRepository
        from app.modules.users.repositories import UserRepository

        self.user = UserRepository(self.session)
        self.category = CategoryRepository(self.session)
        self.location = LocationRepository(self.session)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        await self.session.close()
        self.session = None

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
