# SPDX-FileCopyrightText: Copyright (C) Shaun Wilson
# SPDX-License-Identifier: MIT

from typing import Any
from .DescriptionObject import DescriptionObject


class ServerVariable(DescriptionObject):
    """An object representing a Server Variable for server URL template substitution."""

    def __init__(self, d:dict[str,Any] = None, enum:list[str] = None, default:str = None, description:str = None) -> None:
        super().__init__(d)
        if d is None:
            self.enum = enum
            self.default = default
            self.description = description

    @property
    def enum(self) -> list[str]|None:
        """An enumeration of string values to be used if the substitution options are from a limited set.
        The array MUST NOT be empty."""
        return self.get('enum', None)
    @enum.setter
    def enum(self, v:list[str]|None) -> None:
        if v is None:
            del self['enum']
        else:
            self['enum'] = v

    @property
    def default(self) -> str:
        """REQUIRED. The default value to use for substitution, which SHALL be sent if an alternate value is not supplied. If the enum is defined, the value MUST exist in the enum's values. Note that this behavior is different from the Schema Object's default keyword, which documents the receiver's behavior rather than inserting the value into the data."""
        return self.get('default', None)
    @default.setter
    def default(self, v:str) -> None:
        self['default'] = v

    @property
    def description(self) -> str|None:
        """An optional description for the server variable. CommonMark syntax MAY be used for rich text representation."""
        return self.get('description', None)
    @description.setter
    def description(self, v:str|None) -> None:
        if v is None:
            del self['description']
        else:
            self['description'] = v
