# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .._models import BaseModel

__all__ = ["AssetListResponse", "AssetListResponseItem"]


class AssetListResponseItem(BaseModel):
    artemis_id: str

    symbol: str


AssetListResponse: TypeAlias = List[AssetListResponseItem]
