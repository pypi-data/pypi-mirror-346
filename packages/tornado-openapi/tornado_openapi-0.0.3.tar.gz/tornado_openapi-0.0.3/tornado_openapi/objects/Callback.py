# SPDX-FileCopyrightText: Copyright (C) Shaun Wilson
# SPDX-License-Identifier: MIT

type PathItem = PathItem

from typing import Any
from .DescriptionObject import DescriptionObject
#from .PathItem import PathItem



type Callback = Callback
class Callback(DescriptionObject):
    """
    A map of possible out-of band callbacks related to the parent operation.
    Each value in the map is a Path Item Object that describes a set of requests
    that may be initiated by the API provider and the expected responses. The key
    value used to identify the Path Item Object is an expression, evaluated at runtime,
    that identifies a URL to use for the callback operation.

    ---
    NOTE: Due to the nature of this type there are no properties defined, instead,
    developers accessing this type should prefer indexer syntax, as if it were
    a dictionary of `PathItem` types.
    """

    def __init__(self, d:dict[str,PathItem] = None) -> None:
        super().__init__(d)

    def __getitem__(self, key:str) -> PathItem:
        d = super().get(key, None)
        return None if d is None else PathItem(d)

    def get(self, key:str, default:PathItem = None) -> PathItem|None:
        result = super().get(key, None)
        return default if result is None else PathItem(result)
