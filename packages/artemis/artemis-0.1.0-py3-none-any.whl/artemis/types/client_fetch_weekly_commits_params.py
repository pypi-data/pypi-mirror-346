# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ClientFetchWeeklyCommitsParams"]


class ClientFetchWeeklyCommitsParams(TypedDict, total=False):
    days_back: Annotated[int, PropertyInfo(alias="daysBack")]
    """How many days back from today to pull data for. Data is weekly"""

    ecosystem: str
    """Name of of the ecosystem (ie chain/protocol).

    The full list of names is available from /dev-ecosystems. Omit to fetch data for
    all ecosystems
    """

    include_forks: Annotated[bool, PropertyInfo(alias="includeForks")]
    """If true, count forks in addition to the original repos"""
