# SPDX-FileCopyrightText: Copyright (C) Shaun Wilson
# SPDX-License-Identifier: MIT

from typing import Any
from .DescriptionObject import DescriptionObject
from .Xml import Xml


class Discriminator(DescriptionObject):
    """
    When request bodies or response payloads may be one of a number of different schemas, a Discriminator Object gives a hint about the expected schema of the document. This hint can be used to aid in serialization, deserialization, and validation. The Discriminator Object does this by implicitly or explicitly associating the possible values of a named property with alternative schemas.

    Note that discriminator MUST NOT change the validation outcome of the schema.
    """

    def __init__(self, d:dict[str,Any] = None, propertyName:str = None, xml:Xml = None, mapping:dict[str,str] = None) -> None:
        super().__init__(d)
        if d is None:
            self.propertyName = propertyName
            self.mapping = mapping

    @property
    def propertyName(self) -> str|None:
        """REQUIRED. The name of the property in the payload that will hold the discriminating value. This property SHOULD be required in the payload schema, as the behavior when the property is absent is undefined."""
        return self.get('propertyName', None)
    @propertyName.setter
    def propertyName(self, v:str|None) -> None:
        if v is None:
            del self['propertyName']
        else:
            self['propertyName'] = v.asDictionary()

    @property
    def mapping(self) -> dict[str, str]|None:
        """An object to hold mappings between payload values and schema names or URI references."""
        return self.get('mapping', None)
    @mapping.setter
    def mapping(self, m:dict[str, str]|None) -> None:
        if m is None:
            del self['mapping']
        else:
            self['mapping'] = m
