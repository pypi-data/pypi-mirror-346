# SPDX-FileCopyrightText: Copyright (C) Shaun Wilson
# SPDX-License-Identifier: MIT

from typing import Any
from .Discriminator import Discriminator
from .DescriptionObject import DescriptionObject
from .Example import Example
from .ExternalDocumentation import ExternalDocumentation
from .Xml import Xml


class Schema(DescriptionObject):
    """
    The Schema Object allows the definition of input and output data types. These types can be objects, but also primitives and arrays. This object is a superset of the JSON Schema Specification Draft 2020-12. The empty schema (which allows any instance to validate) MAY be represented by the boolean value true and a schema which allows no instance to validate MAY be represented by the boolean value false.

    For more information about the keywords, see JSON Schema Core and JSON Schema Validation.

    Unless stated otherwise, the keyword definitions follow those of JSON Schema and do not add any additional semantics; this includes keywords such as $schema, $id, $ref, and $dynamicRef being URIs rather than URLs. Where JSON Schema indicates that behavior is defined by the application (e.g. for annotations), OAS also defers the definition of semantics to the application consuming the OpenAPI document.

    ---
    NOTE: Use indexer syntax with this type to set arbitrary keys/etc in the schema defintion. In most cases first-class properties do not exist, especially for this such as companion extensions.
    """

    def __init__(self, d:dict[str,Any] = None, discriminator:Discriminator = None, xml:Xml = None, externalDocs:ExternalDocumentation = None, example:Example = None) -> None:
        super().__init__(d)
        if d is None:
            self.discriminator = discriminator
            self.xml = xml
            self.externalDocs = externalDocs
            self.example = example

    @property
    def discriminator(self) -> Discriminator|None:
        """Adds support for polymorphism. The discriminator is used to determine which of a set of schemas a payload is expected to satisfy. See Composition and Inheritance for more details."""
        v = self.get('discriminator', None)
        return None if v is None else Discriminator(v)
    @discriminator.setter
    def discriminator(self, v:Discriminator|None) -> None:
        if v is None:
            del self['discriminator']
        else:
            self['discriminator'] = v.asDictionary()

    @property
    def xml(self) -> Xml|None:
        """This MAY be used only on property schemas. It has no effect on root schemas. Adds additional metadata to describe the XML representation of this property."""
        v = self.get('xml', None)
        return None if v is None else Xml(v)
    @xml.setter
    def xml(self, v:Xml|None) -> None:
        if v is None:
            del self['xml']
        else:
            self['xml'] = v.asDictionary()

    @property
    def externalDocs(self) -> ExternalDocumentation|None:
        """Additional external documentation for this schema."""
        v = self.get('externalDocs', None)
        return None if v is None else ExternalDocumentation(v)
    @externalDocs.setter
    def externalDocs(self, v:ExternalDocumentation|None) -> None:
        if v is None:
            del self['externalDocs']
        else:
            self['externalDocs'] = v.asDictionary()

    @property
    def example(self) -> Any|None:
        """
        Deprecated: The example field has been deprecated in favor of the JSON Schema examples keyword. Use of example is discouraged, and later versions of this specification may remove it.

        A free-form field to include an example of an instance for this schema. To represent examples that cannot be naturally represented in JSON or YAML, a string value can be used to contain the example with escaping where necessary.
        """
        return self.get('example', None)
    @example.setter
    def example(self, v:Any|None) -> None:
        if v is None:
            del self['example']
        else:
            self['example'] = v
