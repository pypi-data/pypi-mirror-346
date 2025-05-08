# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = ["AssetListMetricsResponse"]


class AssetListMetricsResponse(BaseModel):
    metrics: Optional[List[str]] = None
