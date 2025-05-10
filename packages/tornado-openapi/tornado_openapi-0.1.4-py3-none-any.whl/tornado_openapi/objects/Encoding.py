# SPDX-FileCopyrightText: Copyright (C) Shaun Wilson
# SPDX-License-Identifier: MIT

from typing import Any
from .DescriptionObject import DescriptionObject
from .Header import Header
from .ParameterStyle import ParameterStyle
from .Reference import Reference


class Encoding(DescriptionObject):
    """
    A single encoding definition applied to a single schema property. 

    Properties are correlated with multipart parts using the name parameter of ``Content-Disposition: form-data``, and with ``application/x-www-form-urlencoded`` using the query string parameter names. In both cases, their order is implementation-defined.
    """

    def __init__(self, d:dict[str,Any] = None, contentType:str = None, headers:dict[str,Header] = None, style:ParameterStyle = None, explode:bool = None, allowReserved:bool = None) -> None:
        super().__init__(d)
        if d is None:
            self.contentType = contentType
            self.headers = headers
            self.style = style
            self.explode = explode
            self.allowReserved = allowReserved

    @property
    def contentType(self) -> str|None:
        """The Content-Type for encoding a specific property. The value is a comma-separated list, each element of which is either a specific media type (e.g. ``image/png``) or a wildcard media type (e.g. ``image/*``). Default value depends on the property type as shown in the table below."""
        return self.get('contentType', None)
    @contentType.setter
    def contentType(self, v:str|None) -> None:
        if v is None:
            del self['contentType']
        else:
            self['contentType'] = v

    @property
    def headers(self) -> dict[str, Header|Reference]|None:
        """A map allowing additional information to be provided as headers. Content-Type is described separately and SHALL be ignored in this section. This field SHALL be ignored if the request body media type is not a multipart."""
        m = self.get('headers', None)
        return None if m is None else {
                k:Header(v) if '$ref' not in v else Reference(v)
                for k,v in m.items()
            }
    @headers.setter
    def headers(self, m:dict[str, Header|Reference]|None) -> None:
        if m is None:
            del self['headers']
        else:
            self['headers'] = {
                k:v.asDictionary()
                for k,v in m.items()
            }

    @property
    def style(self) -> ParameterStyle|None:
        """Describes how the parameter value will be serialized depending on the type of the parameter value."""
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
        """When this is true, parameter values are serialized using reserved expansion, as defined by RFC6570, which allows RFC3986's reserved character set, as well as percent-encoded triples, to pass through unchanged, while still percent-encoding all other disallowed characters (including % outside of percent-encoded triples). Applications are still responsible for percent-encoding reserved characters that are not allowed in the query string ([, ], #), or have a special meaning in application/x-www-form-urlencoded (-, &, +). This field only applies to parameters with an in value of query. The default value is false. This field SHALL be ignored if the request body media type is not application/x-www-form-urlencoded or multipart/form-data. If a value is explicitly defined, then the value of contentType (implicit or explicit) SHALL be ignored."""
        return self.get('allowReserved', False)
    @allowReserved.setter
    def allowReserved(self, v:bool|None) -> None:
        if v is None:
            del self['allowReserved']
        else:
            self['allowReserved'] = v
