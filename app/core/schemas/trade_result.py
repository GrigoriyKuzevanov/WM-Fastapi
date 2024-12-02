from datetime import date, datetime

from pydantic import BaseModel


class SpimexTradeResultBase(BaseModel):
    """A base scheme using pydantic model representing trade results. Attributes matches
    sqlalchemy model of trade results.
    """

    model_config = {"from_attributes": True}


class TradeResultOut(SpimexTradeResultBase):
    id: int
    exchange_product_id: str
    exchange_product_name: str
    oil_id: str
    delivery_basis_id: str
    delivery_basis_name: str
    delivery_type_id: str
    volume: int
    total: int
    count: int
    date: date

    created_on: datetime
    updated_on: datetime
