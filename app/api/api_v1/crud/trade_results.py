import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import SpimexTradeResult as trade_result_model


async def read_all_trade_results(
    oil_id: str,
    delivery_type_id: str,
    delivery_basis_id: str,
    limit: int,
    skip: int,
    session: AsyncSession,
) -> list[trade_result_model]:
    """Fetches a list of trade results from the database with given limit and offset.

    Args:
        limit (int): The maximum number of records to retrieve.
        skip (int): The number of records to skip in the database
        oil_id (str): Oil id filter parameter
        delivery_type_id (str): delivery type id filter parameter
        delivery_basis_id (str): delivery basis id filter parameter
        session (AsyncSession): The async database session's instance

    Returns:
        list[trade_result_model]: A list containing trade results model objects
    """

    stmt = select(trade_result_model)

    if oil_id:
        stmt = stmt.filter(trade_result_model.oil_id == oil_id)
    if delivery_type_id:
        stmt = stmt.filter(trade_result_model.delivery_type_id == delivery_type_id)
    if delivery_basis_id:
        stmt = stmt.filter(trade_result_model.delivery_basis_id == delivery_basis_id)

    stmt = stmt.offset(skip).limit(limit)

    db_results = await session.scalars(stmt)

    return db_results.all()


async def read_last_trading_dates(
    days: int, session: AsyncSession
) -> list[datetime.date]:
    """Fetches a list of the most recent distinct trade dates from the database.

    Args:
        days (int): The number of trade dates to fetch
        session (AsyncSession): The async database session's instance

    Returns:
        list[trade_result_model]: A list containing last trade date fields
    """

    date_field = trade_result_model.date
    stmt = select(date_field.distinct()).order_by(date_field.desc()).limit(days)
    db_results = await session.scalars(stmt)

    return db_results.all()


async def read_dynamics(
    start_date: datetime.date,
    end_date: datetime.date,
    oil_id: str,
    delivery_type_id: str,
    delivery_basis_id: str,
    limit: int,
    skip: int,
    session: AsyncSession,
) -> list[trade_result_model]:
    """Fetches a list of trade results from the database within the specified date
    range.

    Args:
        start_date (datetime.date): The start date of quering period
        end_date (datetime.date): The end date of quering period
        limit (int): The maximum number of records to retrieve.
        skip (int): The number of records to skip in the database
        oil_id (str): Oil id filter parameter
        delivery_type_id (str): delivery type id filter parameter
        delivery_basis_id (str): delivery basis id filter parameter
        session (AsyncSession): The async database session's instance

    Returns:
        list[trade_result_model]: A list containing trade results model objects
    """

    stmt = select(trade_result_model).filter(
        trade_result_model.date <= end_date, trade_result_model.date >= start_date
    )

    if oil_id:
        stmt = stmt.filter(trade_result_model.oil_id == oil_id)
    if delivery_type_id:
        stmt = stmt.filter(trade_result_model.delivery_type_id == delivery_type_id)
    if delivery_basis_id:
        stmt = stmt.filter(trade_result_model.delivery_basis_id == delivery_basis_id)

    stmt = stmt.offset(skip).limit(limit)

    db_results = await session.scalars(stmt)

    return db_results.all()
