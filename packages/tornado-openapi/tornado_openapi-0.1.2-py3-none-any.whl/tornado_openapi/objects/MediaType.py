# SPDX-FileCopyrightText: Copyright (C) Shaun Wilson
# SPDX-License-Identifier: MIT

from typing import Any
from .DescriptionObject import DescriptionObject
from .Schema import Schema
from .Encoding import Encoding
from .Example import Example
from .Reference import Reference


class MediaType(DescriptionObject):
    """
    Each Media Type Object provides schema and examples for the media type identified by its key.

    When example or examples are provided, the example SHOULD match the specified schema and be in the correct format as specified by the media type and its encoding. The example and examples fields are mutually exclusive, and if either is present it SHALL override any example in the schema. See Working With Examples for further guidance regarding the different ways of specifying examples, including non-JSON/YAML values.
    """

    def __init__(self, d:dict[str,Any] = None, schema:Schema = None, example:Any = None, examples:dict[str, Example] = None, encoding:dict[str, Encoding] = None) -> None:
        super().__init__(d)
        if d is None:
            self.schema = schema
            self.example = example
            self.examples = examples
            self.encoding = encoding

    @property
    def schema(self) -> Schema|Reference|None:
        """The schema defining the content of the request, response, parameter, or header."""
        d = self.get('schema', None)
        return Schema(d) if '$ref' not in d else Reference(d)
    @schema.setter
    def schema(self, v:Schema|Reference|None) -> None:
        if v is None:
            del self['schema']
        else:
            self['schema'] = v.asDictionary()

    @property
    def example(self) -> Any|None:
        """Example of the media type."""
        return self.get('example', None)
    @example.setter
    def example(self, v:Any|None) -> None:
        if v is None:
            del self['example']
        else:
            self['example'] = v

    @property
    def examples(self) -> dict[str, Example|Reference]|None:
        """Examples of the media type; see Working With Examples."""
        m = self.get('examples', None)
        return None if m is None else {
                k:Example(v) if '$ref' not in v else Reference(v)
                for k,v in m.items()
            }
    @examples.setter
    def examples(self, m:dict[str, Example|Reference]|None) -> None:
        if m is None:
            del self['examples']
        else:
            self['examples'] = {
                k:v.asDictionary()
                for k,v in m.items()
            }

    @property
    def encoding(self) -> dict[str, Encoding]|None:
        """A map between a property name and its encoding information. The key, being the property name, MUST exist in the schema as a property. The encoding field SHALL only apply to Request Body Objects, and only when the media type is multipart or application/x-www-form-urlencoded. If no Encoding Object is provided for a property, the behavior is determined by the default values documented for the Encoding Object."""
        m = self.get('encoding', None)
        return None if m is None else {
                k:Encoding(v)
                for k,v in m.items()
            }
    @encoding.setter
    def encoding(self, m:dict[str, Encoding]|None) -> None:
        if m is None:
            del self['encoding']
        else:
            self['encoding'] = {
                k:v.asDictionary()
                for k,v in m.items()
            }
