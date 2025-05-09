# SPDX-FileCopyrightText: Copyright (C) Shaun Wilson
# SPDX-License-Identifier: MIT

from typing import Any, ForwardRef
from .DescriptionObject import DescriptionObject
from .Reference import Reference
from .Response import Response

Responses = ForwardRef('Responses')


class Responses(DescriptionObject):
    """
    A container for the expected responses of an operation. The container maps a HTTP response code to the expected response.

    The documentation is not necessarily expected to cover all possible HTTP response codes because they may not be known in advance. However, documentation is expected to cover a successful operation response and any known errors.

    The default MAY be used as a default Response Object for all HTTP codes that are not covered individually by the Responses Object.

    The Responses Object MUST contain at least one response code, and if only one response code is provided it SHOULD be the response for a successful operation call.

    ---
    NOTE: Due to the nature of this type developers accessing this type
    should prefer indexer syntax, as if it were a dictionary of ``Response|Reference`` types.
    """

    def __init__(self, d:dict[str,Any] = None, default:Response|Reference = None, codes:dict[str,Response|Reference] = None) -> None:
        super().__init__(d)
        if d is None:
            self.default = default
            self.codes = codes

    @property
    def default(self) -> Response|Reference|None:
        """The documentation of responses other than the ones declared for specific HTTP response codes. Use this field to cover undeclared responses."""
        v = self.get('default', None)
        return None if v is None else Response(v) if '$ref' not in v else Reference(v)
    @default.setter
    def default(self, v:str|None) -> None:
        if v is None:
            del self['default']
        else:
            self['default'] = v

    def __getitem__(self, key:str) -> Response|Reference|None:
        d = super().get(key, None)
        return None if d is None else Response(d) if '$ref' not in d else Reference(d)

    def get(self, key:str, default:Response|Reference|None = None) -> Response|Reference|None:
        result = super().get(key, None)
        return default if result is None else Response(result) if '$ref' not in result else Reference(result)
