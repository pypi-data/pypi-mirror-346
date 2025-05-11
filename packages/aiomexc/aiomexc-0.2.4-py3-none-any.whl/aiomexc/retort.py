from adaptix import NameStyle, Retort, name_mapping

from aiomexc.methods import (
    MexcMethod,
    QueryOrder,
    CreateOrder,
    CreateListenKey,
    GetListenKeys,
    ExtendListenKey,
    DeleteListenKey,
)
from aiomexc.types import (
    Order,
    AccountInformation,
    TickerPrice,
    ListenKey,
    ListenKeys,
    CreateOrder as CreateOrderType,
)

type_recipes = [
    name_mapping(
        mexc_type,
        name_style=NameStyle.CAMEL,
    )
    for mexc_type in [
        Order,
        AccountInformation,
        TickerPrice,
        ListenKey,
        ListenKeys,
        CreateOrderType,
    ]
]

method_recipes = [
    name_mapping(
        MexcMethod,
        name_style=NameStyle.CAMEL,
        omit_default=True,
    ),
    name_mapping(
        QueryOrder,
        name_style=NameStyle.CAMEL,
        omit_default=True,
    ),
    name_mapping(
        CreateListenKey,
        name_style=NameStyle.CAMEL,
        omit_default=True,
    ),
    name_mapping(
        GetListenKeys,
        name_style=NameStyle.CAMEL,
        omit_default=True,
    ),
    name_mapping(
        ExtendListenKey,
        name_style=NameStyle.CAMEL,
        omit_default=True,
    ),
    name_mapping(
        DeleteListenKey,
        name_style=NameStyle.CAMEL,
        omit_default=True,
    ),
    name_mapping(
        CreateOrder,
        name_style=NameStyle.CAMEL,
        omit_default=True,
    ),
]

_retort = Retort(
    recipe=method_recipes + type_recipes,
)

__all__ = ["_retort"]
