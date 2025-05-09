# SPDX-FileCopyrightText: Copyright (C) Shaun Wilson
# SPDX-License-Identifier: MIT

from typing import Any
from .Callback import Callback
from .DescriptionObject import DescriptionObject
from .Parameter import Parameter

from .Server import Server


class Link(DescriptionObject):
    """
    The Link Object represents a possible design-time link for a response. The presence of a link does not guarantee the caller's ability to successfully invoke it, rather it provides a known relationship and traversal mechanism between responses and other operations.

    Unlike dynamic links (i.e. links provided in the response payload), the OAS linking mechanism does not require link information in the runtime response.

    For computing links and providing instructions to execute them, a runtime expression is used for accessing values in an operation and using them as parameters while invoking the linked operation.
    """

    def __init__(self, d:dict[str,Any] = None, operationRef:str = None, operationId:str = None, parameters:dict[str,Any] = None, requestBody:Any = None, description:str = None, server:Server = None) -> None:
        super().__init__(d)
        if d is None:
            self.operationRef = operationRef
            self.operationId = operationId
            self.parameters = parameters
            self.requestBody = requestBody
            self.description = description
            self.server = server

    @property
    def operationRef(self) -> str|None:
        """A URI reference to an OAS operation. This field is mutually exclusive of the operationId field, and MUST point to an Operation Object. Relative operationRef values MAY be used to locate an existing Operation Object in the OpenAPI Description."""
        return self.get('operationRef', None)
    @operationRef.setter
    def operationRef(self, v:str|None) -> None:
        if v is None:
            del self['operationRef']
        else:
            self['operationRef'] = v

    @property
    def operationId(self) -> str|None:
        """The name of an existing, resolvable OAS operation, as defined with a unique operationId. This field is mutually exclusive of the operationRef field."""
        return self.get('operationId', None)
    @operationId.setter
    def operationId(self, v:str|None) -> None:
        if v is None:
            del self['operationId']
        else:
            self['operationId'] = v

    @property
    def parameters(self) -> dict[str,Any]|None:
        """A map representing parameters to pass to an operation as specified with operationId or identified via operationRef. The key is the parameter name to be used (optionally qualified with the parameter location, e.g. path.id for an id parameter in the path), whereas the value can be a constant or an expression to be evaluated and passed to the linked operation."""
        return self.get('parameters', None)
    @parameters.setter
    def parameters(self, m:dict[str,Any]|None) -> None:
        if m is None:
            del self['parameters']
        else:
            self['parameters'] = v

    @property
    def requestBody(self) -> Any|None:
        """A literal value or {expression} to use as a request body when calling the target operation."""
        return self.get('requestBody', None)
    @requestBody.setter
    def requestBody(self, v:Any|None) -> None:
        if v is None:
            del self['requestBody']
        else:
            self['requestBody'] = v

    @property
    def description(self) -> str|None:
        """A description of the link. CommonMark syntax MAY be used for rich text representation."""
        return self.get('description', None)
    @description.setter
    def description(self, v:str|None) -> None:
        if v is None:
            del self['description']
        else:
            self['description'] = v
    
    @property
    def server(self) -> Server|None:
        """A server object to be used by the target operation."""
        v = self.get('server', None)
        return None if v is None else Server(v)
    @server.setter
    def server(self, v:Server|None) -> None:
        if v is None:
            del self['server']
        else:
            self['server'] = v.asDictionary()
