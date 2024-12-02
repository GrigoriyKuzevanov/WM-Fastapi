import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.crud import (
    read_all_trade_results,
    read_dynamics,
    read_last_trading_dates,
)
from core.config import settings
from core.models import db_connector
from core.schemas import TradeResultOut, TradingFilterParams

router = APIRouter(prefix=settings.api.v1.trade_results, tags=["Trade-results"])


@router.get("/", response_model=list[TradeResultOut])
async def get_trading_results(
    filter_query: Annotated[TradingFilterParams, Query()],
    session: AsyncSession = Depends(db_connector.get_session),
) -> list[TradeResultOut]:
    trade_results = await read_all_trade_results(
        oil_id=filter_query.oil_id,
        delivery_type_id=filter_query.delivery_type_id,
        delivery_basis_id=filter_query.delivery_basis_id,
        limit=filter_query.limit,
        skip=filter_query.skip,
        session=session,
    )

    return trade_results


@router.get("/last-dates")
async def get_last_trading_dates(
    days: int = 1,
    session: AsyncSession = Depends(db_connector.get_session),
) -> list[str]:
    trade_dates = await read_last_trading_dates(days, session)

    response = [trade_date.strftime("%d-%m-%Y") for trade_date in trade_dates]

    return response


@router.get("/dynamics", response_model=list[TradeResultOut])
async def get_dynamics(
    start_date: datetime.date,
    end_date: datetime.date,
    session: AsyncSession = Depends(db_connector.get_session),
) -> list[TradeResultOut]:
    trade_results = await read_dynamics(start_date, end_date, session)

    return trade_results
