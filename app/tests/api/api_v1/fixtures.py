from datetime import date, timedelta

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import SpimexTradeResult


@pytest_asyncio.fixture(scope="function")
async def five_test_results(
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
            "exchange_product_id": f"exchange_product_id_test {i}",
            "exchange_product_name": f"exchange_product_name_test {i}",
            "oil_id": f"oil_id_test {i}",
            "delivery_basis_id": f"delivery_basis_id_test {i}",
            "delivery_basis_name": f"delivery_basis_name_test {i}",
            "delivery_type_id": f"delivery_type_id_test {i}",
            "volume": 100 * i,
            "total": 101 * i,
            "count": 102 * i,
            "date": current_date - td,
        }
        trade_results_data.append(data_to_save)

    models = [SpimexTradeResult(**data) for data in trade_results_data]
    test_session.add_all(models)
    await test_session.commit()

    return models
