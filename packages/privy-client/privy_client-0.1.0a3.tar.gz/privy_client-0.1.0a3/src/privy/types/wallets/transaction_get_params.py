# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Optional
from typing_extensions import Literal, Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["TransactionGetParams"]


class TransactionGetParams(TypedDict, total=False):
    asset: Required[Union[Literal["usdc", "eth"], List[Literal["usdc", "eth"]]]]

    chain: Required[Literal["base"]]

    query_wallet_id: Required[Annotated[str, PropertyInfo(alias="wallet_id")]]

    cursor: str

    limit: Optional[float]
