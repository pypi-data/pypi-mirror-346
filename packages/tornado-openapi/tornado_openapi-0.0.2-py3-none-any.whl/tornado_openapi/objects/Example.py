# SPDX-FileCopyrightText: Copyright (C) Shaun Wilson
# SPDX-License-Identifier: MIT

from typing import Any
from .DescriptionObject import DescriptionObject


class Example(DescriptionObject):
    """
    An object grouping an internal or external example value with basic summary and description metadata. This object is typically used in fields named examples (plural), and is a referenceable alternative to older example (singular) fields that do not support referencing or metadata.

    Examples allow demonstration of the usage of properties, parameters and objects within an API.
    """

    def __init__(self, d:dict[str,Any] = None, summary:str = None, description:str = None, value:Any = None, externalValue:str = None, ) -> None:
        super().__init__(d)
        if d is None:
            self.summary = summary
            self.description = description
            self.value = value
            self.externalValue = externalValue

    @property
    def summary(self) -> str|None:
        """Short description for the example."""
        return self.get('summary', None)
    @summary.setter
    def summary(self, v:str|None) -> None:
        if v is None:
            del self['summary']
        else:
            self['summary'] = v

    @property
    def description(self) -> str|None:
        """Long description for the example. CommonMark syntax MAY be used for rich text representation."""
        return self.get('description', None)
    @description.setter
    def description(self, v:str|None) -> None:
        if v is None:
            del self['description']
        else:
            self['description'] = v

    @property
    def value(self) -> Any|None:
        """Embedded literal example. The value field and externalValue field are mutually exclusive. To represent examples of media types that cannot naturally represented in JSON or YAML, use a string value to contain the example, escaping where necessary."""
        return self.get('value', None)
    @value.setter
    def value(self, v:Any|None) -> None:
        if v is None:
            del self['value']
        else:
            self['value'] = v

    @property
    def externalValue(self) -> str|None:
        """A URI that identifies the literal example. This provides the capability to reference examples that cannot easily be included in JSON or YAML documents. The value field and externalValue field are mutually exclusive. See the rules for resolving Relative References."""
        return self.get('externalValue', None)
    @externalValue.setter
    def externalValue(self, v:str|None) -> None:
        if v is None:
            del self['externalValue']
        else:
            self['externalValue'] = v
