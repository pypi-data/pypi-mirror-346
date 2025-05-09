# SPDX-FileCopyrightText: Copyright (C) Shaun Wilson
# SPDX-License-Identifier: MIT

from typing import Any
from .DescriptionObject import DescriptionObject
from .Example import Example
from .MediaType import MediaType
from .ParameterLocation import ParameterLocation
from .ParameterStyle import ParameterStyle
from .Schema import Schema


class Parameter(DescriptionObject):
    """
    Describes a single operation parameter.

    A unique parameter is defined by a combination of a name and location.

    .. note:: Due to Python having `in` as a reserved word, the `in` parameter is renamed `location` on this object. Internally this is still stored as `in` and will be serialized/deserialized as `in`.
    """

    def __init__(self, d:dict[str,Any] = None, name:str = None, location:ParameterLocation = None, description:str = None, required:bool = None, deprecated:bool = None, allowEmptyValue:bool = None, style:ParameterStyle = None, explode:bool = None, allowReserved:bool = None, schema:Schema = None, example:Any = None, examples:dict[str, Example] = None, content:dict[str, MediaType] = None) -> None:
        super().__init__(d)
        if d is None:
            self.name = name
            self.location = location
            self.description = description
            self.required = required
            self.deprecated = deprecated
            self.allowEmptyValue = allowEmptyValue
            self.style = style
            self.explode = explode
            self.allowReserved = allowReserved
            self.schema = schema
            self.example = example
            self.examples = examples
            self.content = content

    @property
    def name(self) -> str:
        """
        REQUIRED. The name of the parameter. Parameter names are case sensitive.
        
        .. Restrictions::
        * If in is "path", the name field MUST correspond to a template expression occurring within the path field in the Paths Object. See Path Templating for further information.
        * If in is "header" and the name field is "Accept", "Content-Type" or "Authorization", the parameter definition SHALL be ignored.
        * For all other cases, the name corresponds to the parameter name used by the in field.
        """
        return self.get('name', None)
    @name.setter
    def name(self, v:str) -> None:
        self['name'] = v

    @property
    def location(self) -> ParameterLocation|None:
        """
        REQUIRED. The location of the parameter. Possible values are "query", "header", "path" or "cookie".

        ---
        This is documented as `in` within the OAS3 specification.
        """
        v = self.get('in', None)
        return None if v is None else ParameterLocation(v)
    @location.setter
    def location(self, v:ParameterLocation|None) -> None:
        if v is None:
            self.pop('in')
        else:
            self['in'] = v.value

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
    def allowEmptyValue(self) -> bool|None:
        """If true, clients MAY pass a zero-length string value in place of parameters that would otherwise be omitted entirely, which the server SHOULD interpret as the parameter being unused. Default value is false. If style is used, and if behavior is n/a (cannot be serialized), the value of allowEmptyValue SHALL be ignored. Interactions between this field and the parameter's Schema Object are implementation-defined. This field is valid only for query parameters. Use of this field is NOT RECOMMENDED, and it is likely to be removed in a later revision."""
        return self.get('allowEmptyValue', False)
    @allowEmptyValue.setter
    def allowEmptyValue(self, v:bool|None) -> None:
        if v is None:
            del self['allowEmptyValue']
        else:
            self['allowEmptyValue'] = v

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
    def allowReserved(self) -> bool|None:
        """When this is true, parameter values are serialized using reserved expansion, as defined by RFC6570, which allows RFC3986's reserved character set, as well as percent-encoded triples, to pass through unchanged, while still percent-encoding all other disallowed characters (including % outside of percent-encoded triples). Applications are still responsible for percent-encoding reserved characters that are not allowed in the query string ([, ], #), or have a special meaning in application/x-www-form-urlencoded (-, &, +); see Appendices C and E for details. This field only applies to parameters with an in value of query. The default value is false."""
        return self.get('allowReserved', False)
    @allowReserved.setter
    def allowReserved(self, v:bool|None) -> None:
        if v is None:
            del self['allowReserved']
        else:
            self['allowReserved'] = v

    @property
    def schema(self) -> Schema|None:
        """The schema defining the type used for the parameter."""
        v = self.get('schema', None)
        return None if v is None else Schema(v)
    @schema.setter
    def schema(self, v:Schema|None) -> None:
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
    def examples(self) -> dict[str, Example]|None:
        """Examples of the parameter's potential value."""
        m = self.get('examples', None)
        return None if m is None else {
                k:Example(v)
                for k,v in m.items()
            }
    @examples.setter
    def examples(self, m:dict[str, Example]|None) -> None:
        if m is None:
            del self['examples']
        else:
            self['examples'] = {
                k:v.asDictionary()
                for k,v in m.items()
            }

    @property
    def content(self) -> dict[str, MediaType]|None:
        """A map containing the representations for the parameter. The key is the media type and the value describes it. The map MUST only contain one entry."""
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
