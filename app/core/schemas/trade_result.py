import datetime
from typing import Any

from pydantic import BaseModel, field_validator


class SpimexTradeResultBase(BaseModel):
    """A base scheme using pydantic model representing trade results. Attributes matches
    sqlalchemy model of trade results.
    """

    model_config = {"from_attributes": True}


class TradeResultDate(SpimexTradeResultBase):
    """A class to represent date of trade with a formatted date."""

    date: str

    @field_validator("date", mode="before")
    @classmethod
    def validate_date(cls, value: Any) -> str:
        """Formats the date value to "DD-MM-YYYY" if it's a "datetime.date" object
        before pydantic main validation.

        Args:
            value (Any): The value to format

        Returns:
            str: String representation of the "datetime.date" object or the original
            value
        """

        if isinstance(value, datetime.date):
            return value.strftime("%d-%m-%Y")
        return value


class TradeResultOut(TradeResultDate):
    """A class to represent trade result record from database with formatted created_on
    and updated_on fields.
    """

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

    created_on: str
    updated_on: str

    @field_validator("created_on", "updated_on", mode="before")
    @classmethod
    def validate_datetime(cls, value: Any) -> str:
        """Formats the datetime value to "DD-MM-YYYY, HH:MM:SS" if it's a
        "datetime.datetime" object before pydantic main validation.

        Args:
            value (Any): The value to format

        Returns:
            str: String representation of the "datetime.datetime" object or the original
            value
        """

        if isinstance(value, datetime.datetime):
            return value.strftime("%d-%m-%Y, %H:%M:%S")
        return value
