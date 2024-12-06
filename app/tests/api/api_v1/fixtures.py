from datetime import date, timedelta

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import SpimexTradeResult


@pytest_asyncio.fixture(scope="function")
async def five_test_dates_results(
    test_session: AsyncSession,
) -> list[SpimexTradeResult]:
    """Creates and adds to testing database five test "SpimexTradeResult" model
    instances.

    Each record has id from 1 to 5 and sequential date field values starting from
    current date.

    Args:
        test_session (AsyncSession): Sqlalchemy async session to testing database

    Returns:
        list[SpimexTradeResult]: A list of "SpimexTradeResult" model instances
    """

    trade_results_data = []
    current_date = date.today()

    for i in range(1, 6):
        td = timedelta(days=i)
        data_to_save = {
            "id": i,
            "exchange_product_id": "exchange_product_id",
            "exchange_product_name": "exchange_product_name",
            "oil_id": "oil_id",
            "delivery_basis_id": "delivery_basis_id",
            "delivery_basis_name": "delivery_basis_name",
            "delivery_type_id": "delivery_type_id",
            "volume": i,
            "total": i,
            "count": i,
            "date": current_date - td,
        }
        trade_results_data.append(data_to_save)

    models = [SpimexTradeResult(**data) for data in trade_results_data]
    test_session.add_all(models)
    await test_session.commit()

    return models
