# SPDX-FileCopyrightText: Copyright (C) Shaun Wilson
# SPDX-License-Identifier: MIT

from typing import Any
from .DescriptionObject import DescriptionObject
from .Parameter import Parameter
from .Reference import Reference
from .Operation import Operation


class PathItem(DescriptionObject):
    """Describes the operations available on a single path. A Path Item MAY be empty, due to ACL constraints. The path itself is still exposed to the documentation viewer but they will not know which operations and parameters are available."""
    
    def __init__(self, d:dict[str,Any] = None, ref:str = None, summary:str = None, description:str = None, get:Operation = None, put:Operation = None, post:Operation = None, delete:Operation = None, options:Operation = None, head:Operation = None, patch:Operation = None, trace:Operation = None, parameters:list[Parameter|Reference] = None) -> None:
        super().__init__(d)
        if d is None:
            self.ref = ref
            self.summary = summary
            self.description = description
            self.get = get
            self.put = put
            self.post = post
            self.delete = delete
            self.options = options
            self.head = head
            self.patch = patch
            self.trace = trace
            self.parameters = parameters

    @property
    def ref(self) -> str|None:
        """
        Allows for a referenced definition of this path item. The value MUST be in the form of a URI, and the referenced structure MUST be in the form of a Path Item Object. In case a Path Item Object field appears both in the defined object and the referenced object, the behavior is undefined. See the rules for resolving Relative References.
        
        WARNING: The behavior of $ref with adjacent properties is likely to change in future versions of this specification to bring it into closer alignment with the behavior of the Reference Object.
        """
        return super().get('$ref', None)
    @ref.setter
    def ref(self, v:str|None) -> None:
        if v is None:
            del self['$ref']
        else:
            self['$ref'] = v

    @property
    def summary(self) -> str|None:
        """An optional string summary, intended to apply to all operations in this path."""
        return super().get('summary', None)
    @summary.setter
    def summary(self, v:str|None) -> None:
        if v is None:
            del self['summary']
        else:
            self['summary'] = v

    @property
    def description(self) -> str|None:
        """An optional string description, intended to apply to all operations in this path. CommonMark syntax MAY be used for rich text representation."""
        return super().get('description', None)
    @description.setter
    def description(self, v:str|None) -> None:
        if v is None:
            del self['description']
        else:
            self['description'] = v

    @property
    def get(self) -> Operation|None:
        """A definition of a GET operation on this path."""
        v = super().get('get', None)
        return None if v is None else Operation(v)
    @get.setter
    def get(self, v:Operation|None) -> None:
        if v is None:
            self.pop('get')
        else:
            self['get'] = v.asDictionary()

    @property
    def put(self) -> Operation|None:
        """A definition of a PUT operation on this path."""
        v = super().get('put', None)
        return None if v is None else Operation(v)
    @put.setter
    def put(self, v:Operation|None) -> None:
        if v is None:
            self.pop('put')
        else:
            self['put'] = v.asDictionary()

    @property
    def post(self) -> Operation|None:
        """A definition of a POST operation on this path."""
        v = super().get('post', None)
        return None if v is None else Operation(v)
    @post.setter
    def post(self, v:Operation|None) -> None:
        if v is None:
            self.pop('post')
        else:
            self['post'] = v.asDictionary()

    @property
    def delete(self) -> Operation|None:
        """A definition of a DELETE operation on this path."""
        v = super().get('delete', None)
        return None if v is None else Operation(v)
    @delete.setter
    def delete(self, v:Operation|None) -> None:
        if v is None:
            self.pop('delete')
        else:
            self['delete'] = v.asDictionary()

    @property
    def options(self) -> Operation|None:
        """A definition of a OPTIONS operation on this path."""
        v = super().get('options', None)
        return None if v is None else Operation(v)
    @options.setter
    def options(self, v:Operation|None) -> None:
        if v is None:
            self.pop('options')
        else:
            self['options'] = v.asDictionary()

    @property
    def head(self) -> Operation|None:
        """A definition of a HEAD operation on this path."""
        v = super().get('head', None)
        return None if v is None else Operation(v)
    @head.setter
    def head(self, v:Operation|None) -> None:
        if v is None:
            self.pop('head')
        else:
            self['head'] = v.asDictionary()

    @property
    def patch(self) -> Operation|None:
        """A definition of a PATCH operation on this path."""
        v = super().get('patch', None)
        return None if v is None else Operation(v)
    @patch.setter
    def patch(self, v:Operation|None) -> None:
        if v is None:
            self.pop('patch')
        else:
            self['patch'] = v.asDictionary()

    @property
    def trace(self) -> Operation|None:
        """A definition of a TRACE operation on this path."""
        v = super().get('trace', None)
        return None if v is None else Operation(v)
    @trace.setter
    def trace(self, v:Operation|None) -> None:
        if v is None:
            self.pop('trace')
        else:
            self['trace'] = v.asDictionary()

    @property
    def parameters(self) -> list[Parameter|Reference]|None:
        """A list of parameters that are applicable for all the operations described under this path. These parameters can be overridden at the operation level, but cannot be removed there. The list MUST NOT include duplicated parameters. A unique parameter is defined by a combination of a name and location. The list can use the Reference Object to link to parameters that are defined in the OpenAPI Object's components.parameters."""
        v = super().get('parameters', None)
        return None if v is None else [
            Parameter(e) if '$ref' not in e else Reference(e)
            for e in v
        ]
    @parameters.setter
    def parameters(self, v:list[Parameter|Reference]|None) -> None:
        if v is None:
            del self['parameters']
        else:
            self['parameters'] = [e.asDictionary() for e in v]
