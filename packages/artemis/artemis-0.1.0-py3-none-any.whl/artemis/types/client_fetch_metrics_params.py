# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from datetime import date
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ClientFetchMetricsParams"]


class ClientFetchMetricsParams(TypedDict, total=False):
    symbols: Required[str]
    """Symbols, comma-separated"""

    end_date: Annotated[Union[str, date], PropertyInfo(alias="endDate", format="iso8601")]
    """End date for time range"""

    start_date: Annotated[Union[str, date], PropertyInfo(alias="startDate", format="iso8601")]
    """Start date for time range"""

    summarize: bool
    """
    When true, will calculate the percent change for a metric from startDate to
    endDate
    """
