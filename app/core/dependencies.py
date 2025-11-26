from app.core.unit_of_work import UnitOfWork


async def get_unit_of_work() -> UnitOfWork:
    return UnitOfWork()
