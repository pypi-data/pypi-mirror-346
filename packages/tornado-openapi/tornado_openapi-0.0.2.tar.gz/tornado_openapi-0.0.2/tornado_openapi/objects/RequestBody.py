# SPDX-FileCopyrightText: Copyright (C) Shaun Wilson
# SPDX-License-Identifier: MIT

from typing import Any
from .DescriptionObject import DescriptionObject
from .MediaType import MediaType


class RequestBody(DescriptionObject):
    """Describes a single request body."""

    def __init__(self, d:dict[str,Any] = None, description:str = None, content:dict[str,MediaType] = None, required:bool = None) -> None:
        super().__init__(d)
        if d is None:
            self.description = description
            self.content = content
            self.required = required

    @property
    def description(self) -> str|None:
        """A brief description of the request body. This could contain examples of use. CommonMark syntax MAY be used for rich text representation."""
        return self.get('description', None)
    @description.setter
    def description(self, v:str|None) -> None:
        if v is None:
            del self['description']
        else:
            self['description'] = v

    @property
    def content(self) -> dict[str, MediaType]:
        """REQUIRED. The content of the request body. The key is a media type or media type range and the value describes it. For requests that match multiple keys, only the most specific key is applicable. e.g. "text/plain" overrides "text/*"."""
        m = self.get('content', None)
        return None if m is None else {
                k:MediaType(v)
                for k,v in m.items()
            }
    @content.setter
    def content(self, m:dict[str, MediaType]) -> None:
        if m is None:
            self['content'] = {}
        else:
            self['content'] = {
                k:v.asDictionary()
                for k,v in m.items()
            }

    @property
    def required(self) -> bool|None:
        """Determines if the request body is required in the request. Defaults to false."""
        return self.get('required', False)
    @required.setter
    def required(self, v:bool|None) -> None:
        if v is None:
            del self['required']
        else:
            self['required'] = v
