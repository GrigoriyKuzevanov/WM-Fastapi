from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.crud import read_all_trade_results, read_last_trading_dates
from core.config import settings
from core.models import db_connector
from core.schemas import TradeResultOut

router = APIRouter(prefix=settings.api.v1.trade_results, tags=["Trade-results"])


@router.get("", response_model=list[TradeResultOut])
async def get_trade_results(
    limit: int = 10,
    skip: int = 0,
    session: AsyncSession = Depends(db_connector.get_session),
) -> list[TradeResultOut]:
    trade_results = await read_all_trade_results(limit, skip, session)

    return trade_results


@router.get("/last-dates")
async def get_last_trading_dates(
    days: int = 1,
    session: AsyncSession = Depends(db_connector.get_session),
) -> list[str]:
    trade_dates = await read_last_trading_dates(days, session)

    response = [trade_date.strftime("%d-%m-%Y") for trade_date in trade_dates]

    return response
