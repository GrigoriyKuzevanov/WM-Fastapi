import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.crud import (
    read_all_trade_results,
    read_dynamics,
    read_last_trading_dates,
)
from core.config import settings
from core.models import db_connector
from core.redis import request_key_builder
from core.schemas import DynamicsFilterParams, TradeResultOut, TradingFilterParams

router = APIRouter(prefix=settings.api.v1.trade_results, tags=["Trade-results"])

cache_expiration = 60 * 60 * 24


@router.get("/", response_model=list[TradeResultOut])
@cache(expire=cache_expiration, key_builder=request_key_builder)
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
@cache(expire=cache_expiration, key_builder=request_key_builder)
async def get_last_trading_dates(
    days: int = Query(1, gt=0, description="The number of days to get dates for"),
    session: AsyncSession = Depends(db_connector.get_session),
) -> list[datetime.date]:
    trade_dates = await read_last_trading_dates(days, session)

    return trade_dates


@router.get("/dynamics", response_model=list[TradeResultOut])
@cache(expire=cache_expiration, key_builder=request_key_builder)
async def get_dynamics(
    filter_query: Annotated[DynamicsFilterParams, Query()],
    session: AsyncSession = Depends(db_connector.get_session),
) -> list[TradeResultOut]:
    trade_results = await read_dynamics(
        start_date=filter_query.start_date,
        end_date=filter_query.end_date,
        oil_id=filter_query.oil_id,
        delivery_type_id=filter_query.delivery_type_id,
        delivery_basis_id=filter_query.delivery_basis_id,
        limit=filter_query.limit,
        skip=filter_query.skip,
        session=session,
    )

    return trade_results
