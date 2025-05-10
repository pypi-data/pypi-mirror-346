# SPDX-FileCopyrightText: Copyright (C) Shaun Wilson
# SPDX-License-Identifier: MIT

from typing import Any
from .DescriptionObject import DescriptionObject


class License(DescriptionObject):
    """License information for the exposed API."""

    def __init__(self, d:dict[str,Any] = None, name:str = None, identifier:str = None, url:str = None) -> None:
        super().__init__(d)
        if d is None:
            self.name = name
            self.identifier = identifier
            self.url = url

    @property
    def name(self) -> str:
        """REQUIRED. The license name used for the API."""
        return self.get('name', None)
    @name.setter
    def name(self, v:str) -> None:
        self['name'] = v

    @property
    def identifier(self) -> str|None:
        """An SPDX license expression for the API. The identifier field is mutually exclusive of the url field."""
        return self.get('identifier', None)
    @identifier.setter
    def identifier(self, v:str|None) -> None:
        if v is None:
            del self['identifier']
        else:
            self['identifier'] = v

    @property
    def url(self) -> str|None:
        """A URI for the license used for the API. This MUST be in the form of a URI. The url field is mutually exclusive of the identifier field."""
        return self.get('url', None)
    @url.setter
    def url(self, v:str|None) -> None:
        if v is None:
            del self['url']
        else:
            self['url'] = v
