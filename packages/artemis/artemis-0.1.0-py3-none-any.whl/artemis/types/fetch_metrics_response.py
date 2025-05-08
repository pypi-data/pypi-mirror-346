# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = ["FetchMetricsResponse", "Data"]


class Data(BaseModel):
    artemis_ids: Optional[List[object]] = None

    symbols: Optional[List[object]] = None


class FetchMetricsResponse(BaseModel):
    data: Optional[Data] = None
