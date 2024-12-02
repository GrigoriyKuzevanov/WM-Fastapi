import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator


class FilterParamsBase(BaseModel):
    """A base scheme using pydantic model for query params using to filter database
    query.
    """

    limit: int = Field(10, ge=0, description="Limit to returning results")
    skip: int = Field(0, ge=0, description="Offset to skip in returning results")


class TradingFilterParams(FilterParamsBase):
    """A pydantic model for query params using to filter spimex trade results."""

    oil_id: str | None = Field(None, description="Oil id")
    delivery_type_id: str | None = Field(None, description="Id of delivery type")
    delivery_basis_id: str | None = Field(None, description="Id of delivery bases")


class DynamicsFilterParams(TradingFilterParams):
    """A pydantic model for query params using to get trade results for the period"""

    start_date: datetime.date = Field(description="The start date for period")
    end_date: datetime.date = Field(
        datetime.date.today(), description="The end date for period"
    )


class SpimexTradeResultBase(BaseModel):
    """A base scheme using pydantic model representing trade results. Attributes matches
    sqlalchemy model of trade results.
    """

    model_config = {"from_attributes": True}


class TradeResultOut(SpimexTradeResultBase):
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
    date: str

    created_on: str
    updated_on: str

    @field_validator("created_on", "updated_on", "date", mode="before")
    @classmethod
    def validate_datetime(cls, value: Any) -> str:
        """Formats the "datetime" values to specific formate before pydantic main
        validation:
        "DD-MM-YYYY, HH:MM:SS" if it's a datetime.datetime value
        "DD-MM-YYYY" if it's a datetime.date value
        In others cases - return original value.

        Args:
            value (Any): The value to format

        Returns:
            str: String representation of the "datetime.datetime" object or the original
            value
        """

        if isinstance(value, datetime.datetime):
            return value.strftime("%d-%m-%Y, %H:%M:%S")
        if isinstance(value, datetime.date):
            return value.strftime("%d-%m-%Y")
        return value
