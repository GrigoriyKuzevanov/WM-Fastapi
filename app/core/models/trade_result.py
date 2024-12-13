import datetime

from sqlalchemy import Date
from sqlalchemy.orm import Mapped, mapped_column

from core.config import settings

from .base import Base


class SpimexTradeResult(Base):
    """A class to represent record of trading results on SPIMEX

    Attributes:
        exchange_product_id (str): The unique identifier for the traded exchange product
        exchange_product_name (str): The name of the traded exchange product
        oil_id (str): The identifier for the type of oil traded
        delivery_basis_id (str): The identifier for the delivery basis
        delivery_basis_name (str): The name of the delivery basis
        delivery_type_id (str): The identifier for the type of delivery
        volume (int): The volume of the trade
        total (int): The total value of the trade in monetary units
        count (int): The number of transactions in the trade
        date (datetime.date): The date of the trade
    """

    __tablename__ = settings.main_pg_db.spimex_trade_result_tablename

    exchange_product_id: Mapped[str]
    exchange_product_name: Mapped[str]
    oil_id: Mapped[str]
    delivery_basis_id: Mapped[str]
    delivery_basis_name: Mapped[str]
    delivery_type_id: Mapped[str]
    volume: Mapped[int]
    total: Mapped[int]
    count: Mapped[int]
    date: Mapped[datetime.date] = mapped_column(Date)
