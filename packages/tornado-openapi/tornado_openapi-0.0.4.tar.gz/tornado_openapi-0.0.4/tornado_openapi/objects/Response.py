# SPDX-FileCopyrightText: Copyright (C) Shaun Wilson
# SPDX-License-Identifier: MIT

from typing import Any
from .DescriptionObject import DescriptionObject
from .Header import Header
from .Link import Link
from .MediaType import MediaType
from .Reference import Reference


class Response(DescriptionObject):
    """
    Describes a single response from an API operation, including design-time, static links to operations based on the response.
    """

    def __init__(self, d:dict[str,Any] = None, description:str = None, headers:dict[str,Header|Reference] = None, content:dict[str|MediaType] = None, links:dict[str,Link|Reference] = None) -> None:
        super().__init__(d)
        if d is None:
            self.description = description
            self.headers = headers
            self.content = content
            self.links = links

    @property
    def description(self) -> str:
        """REQUIRED. A description of the response. CommonMark syntax MAY be used for rich text representation."""
        return self.get('description', None)
    @description.setter
    def description(self, v:str) -> None:
        self['description'] = v

    @property
    def headers(self) -> dict[str, Header|Reference]|None:
        """Maps a header name to its definition. RFC7230 states header names are case insensitive. If a response header is defined with the name "Content-Type", it SHALL be ignored."""
        m = self.get('headers', None)
        return None if m is None else {
                k:Header(v) if '$ref' not in v else Reference(v)
                for k,v in m.items()
            }
    @headers.setter
    def headers(self, m:dict[str, Header|Reference]|None) -> None:
        if m is None:
            del self['headers']
        else:
            self['headers'] = {
                k:v.asDictionary()
                for k,v in m.items()
            }

    @property
    def content(self) -> dict[str, MediaType]|None:
        """A map containing descriptions of potential response payloads. The key is a media type or media type range and the value describes it. For responses that match multiple keys, only the most specific key is applicable. e.g. ``"text/plain"`` overrides ``"text/*"``."""
        m = self.get('content', None)
        return None if m is None else {
                k:MediaType(v)
                for k,v in m.items()
            }
    @content.setter
    def content(self, m:dict[str, MediaType]|None) -> None:
        if m is None:
            del self['content']
        else:
            self['content'] = {
                k:v.asDictionary()
                for k,v in m.items()
            }

    @property
    def links(self) -> dict[str, Link|Reference]|None:
        """A map of operations links that can be followed from the response. The key of the map is a short name for the link, following the naming constraints of the names for Component Objects."""
        m = self.get('links', None)
        return None if m is None else {
                k:Link(v) if '$ref' not in v else Reference(v)
                for k,v in m.items()
            }
    @links.setter
    def links(self, m:dict[str, Link|Reference]|None) -> None:
        if m is None:
            del self['links']
        else:
            self['links'] = {
                k:v.asDictionary()
                for k,v in m.items()
            }
