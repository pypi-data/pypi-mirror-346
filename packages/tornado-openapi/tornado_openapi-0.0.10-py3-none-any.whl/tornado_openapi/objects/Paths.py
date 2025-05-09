# SPDX-FileCopyrightText: Copyright (C) Shaun Wilson
# SPDX-License-Identifier: MIT

from typing import ForwardRef
from .DescriptionObject import DescriptionObject
from .PathItem import PathItem

Paths = ForwardRef('Paths')


class Paths(DescriptionObject):
    """
    Holds the relative paths to the individual endpoints and their operations.
    The path is appended to the URL from the Server Object in order to construct the full URL.
    The Paths Object MAY be empty, due to Access Control List (ACL) constraints.

    ---
    NOTE: Due to the nature of this type there are no properties defined, instead,
    developers accessing this type should prefer indexer syntax, as if it were
    a dictionary of :py:class:`~tornado.objects.PathItem` types.
    """

    def __init__(self, paths:dict[str,PathItem] = None) -> None:
        super().__init__(paths)

    def __getitem__(self, key:str) -> PathItem|None:
        d = super().get(key, None)
        return None if d is None else PathItem(d)

    def get(self, key:str, default:PathItem = None) -> PathItem|None:
        result = super().get(key, None)
        return default if result is None else PathItem(result)
