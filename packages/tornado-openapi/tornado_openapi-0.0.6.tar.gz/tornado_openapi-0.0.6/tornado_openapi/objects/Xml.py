# SPDX-FileCopyrightText: Copyright (C) Shaun Wilson
# SPDX-License-Identifier: MIT

from typing import Any
from .DescriptionObject import DescriptionObject


class Xml(DescriptionObject):
    """
    A metadata object that allows for more fine-tuned XML model definitions.

    When using arrays, XML element names are not inferred (for singular/plural forms) and the name field SHOULD be used to add that information. See examples for expected behavior.
    """

    def __init__(self, d:dict[str,Any] = None, name:str = None, namespace:str = None, prefix:str = None, attribute:bool = None, wrapped:bool = None) -> None:
        super().__init__(d)
        if d is None:
            self.name = name
            self.namespace = namespace
            self.prefix = prefix
            self.attribute = attribute
            self.wrapped = wrapped

    @property
    def name(self) -> str|None:
        """Replaces the name of the element/attribute used for the described schema property. When defined within items, it will affect the name of the individual XML elements within the list. When defined alongside type being "array" (outside the items), it will affect the wrapping element if and only if wrapped is true. If wrapped is false, it will be ignored."""
        return self.get('name', None)
    @name.setter
    def name(self, v:str|None) -> None:
        if v is None:
            del self['name']
        else:
            self['name'] = v

    @property
    def namespace(self) -> str|None:
        """The URI of the namespace definition. Value MUST be in the form of a non-relative URI."""
        return self.get('namespace', None)
    @namespace.setter
    def namespace(self, v:str|None) -> None:
        if v is None:
            del self['namespace']
        else:
            self['namespace'] = v

    @property
    def prefix(self) -> str|None:
        """The prefix to be used for the name."""
        return self.get('prefix', None)
    @prefix.setter
    def prefix(self, v:str|None) -> None:
        if v is None:
            del self['prefix']
        else:
            self['prefix'] = v

    @property
    def attribute(self) -> bool|None:
        """Declares whether the property definition translates to an attribute instead of an element. Default value is false."""
        return self.get('attribute', False)
    @attribute.setter
    def attribute(self, v:bool|None) -> None:
        if v is None:
            del self['attribute']
        else:
            self['attribute'] = v

    @property
    def wrapped(self) -> bool|None:
        """MAY be used only for an array definition. Signifies whether the array is wrapped (for example, <books><book/><book/></books>) or unwrapped (<book/><book/>). Default value is false. The definition takes effect only when defined alongside type being "array" (outside the items)."""
        return self.get('wrapped', False)
    @wrapped.setter
    def wrapped(self, v:bool|None) -> None:
        if v is None:
            del self['wrapped']
        else:
            self['wrapped'] = v
