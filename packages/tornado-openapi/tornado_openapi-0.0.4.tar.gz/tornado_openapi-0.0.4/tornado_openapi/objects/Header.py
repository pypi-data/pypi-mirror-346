# SPDX-FileCopyrightText: Copyright (C) Shaun Wilson
# SPDX-License-Identifier: MIT

type MediaType = MediaType

from typing import Any
from .DescriptionObject import DescriptionObject
from .Example import Example
#from .MediaType import MediaType
from .ParameterStyle import ParameterStyle
from .Reference import Reference
from .Schema import Schema


class Header(DescriptionObject):
    """
    Describes a single header for HTTP responses and for individual parts in multipart representations; see the relevant Response Object and Encoding Object documentation for restrictions on which headers can be described.

    The Header Object follows the structure of the Parameter Object, including determining its serialization strategy based on whether schema or content is present, with the following changes:

    * ``name`` MUST NOT be specified, it is given in the corresponding headers map.
    * ``in`` MUST NOT be specified, it is implicitly in header.
    * All traits that are affected by the location MUST be applicable to a location of header (for example, ``style``). This means that ``allowEmptyValue`` and ``allowReserved`` MUST NOT be used, and ``style``, if used, MUST be limited to ``"simple"``.
    """

    def __init__(self, d:dict[str,Any] = None, description:str = None, required:bool = None, deprecated:bool = None, style:ParameterStyle = None, explode:bool = None, schema:Schema|Reference = None, example:Any = None, examples:dict[str, Example] = None, content:dict[str, MediaType] = None) -> None:
        super().__init__(d)
        if d is None:
            self.description = description
            self.required = required
            self.deprecated = deprecated
            self.style = style
            self.explode = explode
            self.schema = schema
            self.example = example
            self.examples = examples
            self.content = content

    @property
    def description(self) -> str|None:
        """A brief description of the parameter. This could contain examples of use. CommonMark syntax MAY be used for rich text representation."""
        return self.get('description', None)
    @description.setter
    def description(self, v:str|None) -> None:
        if v is None:
            del self['description']
        else:
            self['description'] = v

    @property
    def required(self) -> bool|None:
        """Determines whether this parameter is mandatory. If the parameter location is "path", this field is REQUIRED and its value MUST be true. Otherwise, the field MAY be included and its default value is false."""
        return self.get('required', False)
    @required.setter
    def required(self, v:bool|None) -> None:
        if v is None:
            del self['required']
        else:
            self['required'] = v

    @property
    def deprecated(self) -> bool|None:
        """Specifies that a parameter is deprecated and SHOULD be transitioned out of usage. Default value is false."""
        return self.get('deprecated', False)
    @deprecated.setter
    def deprecated(self, v:bool|None) -> None:
        if v is None:
            del self['deprecated']
        else:
            self['deprecated'] = v

    @property
    def style(self) -> ParameterStyle|None:
        """Describes how the parameter value will be serialized depending on the type of the parameter value. Default values (based on value of in): for "query" - "form"; for "path" - "simple"; for "header" - "simple"; for "cookie" - "form"."""
        v = self.get('style', None)
        return None if v is None else ParameterStyle(v)
    @style.setter
    def style(self, v:ParameterStyle|None) -> None:
        if v is None:
            self.pop('style')
        else:
            self['style'] = v.value

    @property
    def explode(self) -> bool|None:
        """When this is true, parameter values of type array or object generate separate parameters for each value of the array or key-value pair of the map. For other types of parameters this field has no effect. When style is "form", the default value is true. For all other styles, the default value is false. Note that despite false being the default for deepObject, the combination of false with deepObject is undefined."""
        return self.get('explode', False)
    @explode.setter
    def explode(self, v:bool|None) -> None:
        if v is None:
            del self['explode']
        else:
            self['explode'] = v

    @property
    def schema(self) -> Schema|Reference|None:
        """The schema defining the type used for the parameter."""
        v = super().get('schema', None)
        return None if v is None else Schema(v) if '$ref' not in v else Reference(v)
    @schema.setter
    def schema(self, v:Schema|Reference|None) -> None:
        if v is None:
            del self['schema']
        else:
            self['schema'] = v.asDictionary()

    @property
    def example(self) -> Any|None:
        """Example of the parameter's potential value."""
        return self.get('example', None)
    @example.setter
    def example(self, v:Any|None) -> None:
        if v is None:
            del self['example']
        else:
            self['example'] = v

    @property
    def examples(self) -> dict[str,Example]|None:
        """Examples of the parameter's potential value."""
        m = self.get('examples', None)
        return None if m is None else {
                k:Example(v)
                for k,v in m.items()
            }
    @examples.setter
    def examples(self, m:dict[str,Example]|None) -> None:
        if m is None:
            del self['examples']
        else:
            self['examples'] = {
                k:v.asDictionary()
                for k,v in m.items()
            }

    @property
    def content(self) -> dict[str,MediaType]|None:
        """A map containing the representations for the parameter. The key is the media type and the value describes it. The map MUST only contain one entry."""
        m = self.get('content', None)
        return None if m is None else {
                k:MediaType(v)
                for k,v in m.items()
            }
    @content.setter
    def content(self, m:dict[str,MediaType]|None) -> None:
        if m is None:
            del self['content']
        else:
            self['content'] = {
                k:v.asDictionary()
                for k,v in m.items()
            }
