# SPDX-FileCopyrightText: Copyright (C) Shaun Wilson
# SPDX-License-Identifier: MIT

from typing import Any
from .DescriptionObject import DescriptionObject
from .ServerVariable import ServerVariable


class Server(DescriptionObject):
    """An object representing a Server."""

    def __init__(self, d:dict[str,Any] = None, url:str = None, description:str = None, variables:dict[str, ServerVariable] = None) -> None:
        super().__init__(d)
        if d is None:
            self.url = url
            self.description = description
            self.variables = variables

    @property
    def url(self) -> str:
        """REQUIRED. A URL to the target host. This URL supports Server Variables and MAY be relative, to indicate that the host location is relative to the location where the document containing the Server Object is being served. Variable substitutions will be made when a variable is named in {braces}."""
        return self.get('url', None)
    @url.setter
    def url(self, v:str) -> None:
        self['url'] = v

    @property
    def description(self) -> str|None:
        """An optional string describing the host designated by the URL. CommonMark syntax MAY be used for rich text representation."""
        return self.get('description', None)
    @description.setter
    def description(self, v:str|None) -> None:
        if v is None:
            del self['description']
        else:
            self['description'] = v

    @property
    def variables(self) -> dict[str, ServerVariable]|None:
        """A map between a variable name and its value. The value is used for substitution in the server's URL template."""
        m = self.get('variables', None)
        return None if m is None else {
                k:ServerVariable(v)
                for k,v in m.items()
            }
    @variables.setter
    def variables(self, m:dict[str, ServerVariable]|None) -> None:
        if m is None:
            del self['variables']
        else:
            self['variables'] = {
                k:v.asDictionary()
                for k,v in m.items()
            }
