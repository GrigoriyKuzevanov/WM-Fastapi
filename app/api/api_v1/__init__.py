from fastapi import APIRouter

from core.config import settings

from .trade_results import router as trade_results_router

router = APIRouter(prefix=settings.api.v1.prefix)
router.include_router(trade_results_router)
