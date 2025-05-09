# SPDX-FileCopyrightText: Copyright (C) Shaun Wilson
# SPDX-License-Identifier: MIT

from typing import ForwardRef
from .DescriptionObject import DescriptionObject

SecurityRequirement = ForwardRef('SecurityRequirement')


class SecurityRequirement(DescriptionObject):
    """
    Lists the required security schemes to execute this operation. The name used for each property MUST correspond to a security scheme declared in the Security Schemes under the Components Object.

    A Security Requirement Object MAY refer to multiple security schemes in which case all schemes MUST be satisfied for a request to be authorized. This enables support for scenarios where multiple query parameters or HTTP headers are required to convey security information.

    When the security field is defined on the OpenAPI Object or Operation Object and contains multiple Security Requirement Objects, only one of the entries in the list needs to be satisfied to authorize the request. This enables support for scenarios where the API allows multiple, independent security schemes.

    An empty Security Requirement Object ({}) indicates anonymous access is supported.

    ---
    NOTE: Due to the nature of this type there are no properties defined, instead,
    developers accessing this type should prefer indexer syntax, as if it were
    a dictionary of `list[str]` types.
    """

    def __init__(self, requirements:dict[str,list[str]] = None) -> None:
        super().__init__(requirements)

    def __getitem__(self, key:str) -> list[str]:
        return super().get(key, None)

    def get(self, key:str, default:list[str] = None) -> list[str]|None:
        result = super().get(key, None)
        return default if result is None else result
