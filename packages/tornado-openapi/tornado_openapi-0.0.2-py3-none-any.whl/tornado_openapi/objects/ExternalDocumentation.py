# SPDX-FileCopyrightText: Copyright (C) Shaun Wilson
# SPDX-License-Identifier: MIT

from typing import Any
from .DescriptionObject import DescriptionObject


class ExternalDocumentation(DescriptionObject):
    """Allows referencing an external resource for extended documentation."""

    def __init__(self, d:dict[str,Any] = None, description:str = None, url:str = None) -> None:
        super().__init__(d)
        if d is None:
            self.description = description
            self.url = url

    @property
    def description(self) -> str|None:
        """A description of the target documentation. CommonMark syntax MAY be used for rich text representation."""
        return self.get('description', None)
    @description.setter
    def description(self, v:str|None) -> None:
        if v is None:
            del self['description']
        else:
            self['description'] = v

    @property
    def url(self) -> str:
        """REQUIRED. The URI for the target documentation. This MUST be in the form of a URI."""
        return self.get('url', None)
    @url.setter
    def url(self, v:str) -> None:
        if v is None:
            del self['url']
        else:
            self['url'] = v
