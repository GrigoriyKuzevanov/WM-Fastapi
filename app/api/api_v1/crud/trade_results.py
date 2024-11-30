from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import SpimexTradeResult as trade_result_model


async def read_all_trade_results(
    limit: int, skip: int, session: AsyncSession
) -> list[trade_result_model]:
    """Fetches a list of trade results from the database with given limit and offset.

    Args:
        limit (int): The maximum number of records to retrieve.
        skip (int): The number of records to skip in the database
        session (AsyncSession): The async database session's instance

    Returns:
        list[trade_result_model]: A list containing trade results model objects
    """

    stmt = select(trade_result_model).offset(skip).limit(limit)
    db_results = await session.scalars(stmt)

    return db_results.all()
