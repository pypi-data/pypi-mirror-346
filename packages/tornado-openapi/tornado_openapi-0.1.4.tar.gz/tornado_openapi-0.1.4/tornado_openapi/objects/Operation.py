# SPDX-FileCopyrightText: Copyright (C) Shaun Wilson
# SPDX-License-Identifier: MIT

from typing import Any
from .Callback import Callback
from .DescriptionObject import DescriptionObject
from .ExternalDocumentation import ExternalDocumentation
from .Parameter import Parameter
from .Reference import Reference
from .RequestBody import RequestBody
from .Responses import Responses
from .SecurityRequirement import SecurityRequirement
from .Server import Server


class Operation(DescriptionObject):
    """Describes a single API operation on a path."""

    def __init__(self, d:dict[str,Any] = None, tags:list[str] = None, summary:str = None, description:str = None, externalDocs:ExternalDocumentation = None, operationId:str = None, parameters:list[Parameter|Reference] = None, requestBody:RequestBody|Reference = None, responses:Responses = None, callbacks:dict[str, Callback|Reference] = None, deprecated:bool = None, security:list[SecurityRequirement] = None, servers:list[Server] = None) -> None:
        super().__init__(d)
        if d is None:
            self.tags = tags
            self.summary = summary
            self.description = description
            self.externalDocs = externalDocs
            self.operationId = operationId
            self.parameters = parameters
            self.requestBody = requestBody
            self.responses = responses
            self.callbacks = callbacks
            self.deprecated = deprecated
            self.security = security
            self.servers = servers

    @property
    def tags(self) -> list[str]|None:
        """A list of tags for API documentation control. Tags can be used for logical grouping of operations by resources or any other qualifier."""
        return self['tags']
    @tags.setter
    def tags(self, v:list[str]|None) -> None:
        if v is None:
            del self['tags']
        else:
            self['tags'] = v

    @property
    def summary(self) -> str|None:
        """A short summary of what the operation does"""
        return self.get('summary', None)
    @summary.setter
    def summary(self, v:str|None) -> None:
        if v is None:
            del self['summary']
        else:
            self['summary'] = v

    @property
    def description(self) -> str|None:
        """A verbose explanation of the operation behavior. CommonMark syntax MAY be used for rich text representation."""
        return self.get('description', None)
    @description.setter
    def description(self, v:str|None) -> None:
        if v is None:
            del self['description']
        else:
            self['description'] = v

    @property
    def externalDocs(self) -> ExternalDocumentation|None:
        """Additional external documentation for this operation."""
        v = self.get('externalDocs', None)
        return None if v is None else ExternalDocumentation(v)
    @externalDocs.setter
    def externalDocs(self, v:ExternalDocumentation|None) -> None:
        if v is None:
            del self['externalDocs']
        else:
            self['externalDocs'] = v.asDictionary()

    @property
    def operationId(self) -> str|None:
        """Unique string used to identify the operation. The id MUST be unique among all operations described in the API. The operationId value is case-sensitive. Tools and libraries MAY use the operationId to uniquely identify an operation, therefore, it is RECOMMENDED to follow common programming naming conventions."""
        return self.get('operationId', None)
    @operationId.setter
    def operationId(self, v:str|None) -> None:
        if v is None:
            del self['operationId']
        else:
            self['operationId'] = v

    @property
    def parameters(self) -> list[Parameter|Reference]|None:
        """A list of parameters that are applicable for this operation. If a parameter is already defined at the Path Item, the new definition will override it but can never remove it. The list MUST NOT include duplicated parameters. A unique parameter is defined by a combination of a name and location. The list can use the Reference Object to link to parameters that are defined in the OpenAPI Object's components.parameters."""
        v = self.get('parameters', None)
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

    @property
    def requestBody(self) -> RequestBody|Reference|None:
        """The request body applicable for this operation. The requestBody is fully supported in HTTP methods where the HTTP 1.1 specification RFC7231 has explicitly defined semantics for request bodies. In other cases where the HTTP spec is vague (such as GET, HEAD and DELETE), requestBody is permitted but does not have well-defined semantics and SHOULD be avoided if possible."""
        v = self.get('requestBody', None)
        return None if v is None else RequestBody(v) if '$ref' not in v else Reference(v)
    @requestBody.setter
    def requestBody(self, v:RequestBody|Reference|None) -> None:
        if v is None:
            del self['requestBody']
        else:
            self['requestBody'] = v.asDictionary()

    @property
    def responses(self) -> Responses|None:
        """The list of possible responses as they are returned from executing this operation."""
        v = self.get('responses', None)
        return Responses(v)
    @responses.setter
    def responses(self, v:Responses|None) -> None:
        if v is None:
            del self['responses']
        else:
            self['responses'] = v.asDictionary()

    @property
    def callbacks(self) -> dict[str, Callback|Reference]|None:
        """A map of possible out-of band callbacks related to the parent operation. The key is a unique identifier for the Callback Object. Each value in the map is a Callback Object that describes a request that may be initiated by the API provider and the expected responses."""
        m = self.get('callbacks', None)
        return None if m is None else {
                k:Callback(v) if '$ref' not in v else Reference(v)
                for k,v in m.items()
            }
    @callbacks.setter
    def callbacks(self, m:dict[str, Callback|Reference]|None) -> None:
        if m is None:
            del self['callbacks']
        else:
            self['callbacks'] = {
                k:v.asDictionary()
                for k,v in m.items()
            }

    @property
    def deprecated(self) -> bool|None:
        """Declares this operation to be deprecated. Consumers SHOULD refrain from usage of the declared operation. Default value is false."""
        return self.get('deprecated', None)
    @deprecated.setter
    def deprecated(self, v:bool|None) -> None:
        if v is None:
            del self['deprecated']
        else:
            self['deprecated'] = v

    @property
    def security(self) -> list[SecurityRequirement]|None:
        """A declaration of which security mechanisms can be used for this operation. The list of values includes alternative Security Requirement Objects that can be used. Only one of the Security Requirement Objects need to be satisfied to authorize a request. To make security optional, an empty security requirement ({}) can be included in the array. This definition overrides any declared top-level security. To remove a top-level security declaration, an empty array can be used."""
        return [SecurityRequirement(e) for e in self.get('security', None)]
    @security.setter
    def security(self, v:list[SecurityRequirement]|None) -> None:
        if v is None:
            del self['security']
        else:
            self['security'] = [e.asDictionary() for e in v]

    @property
    def servers(self) -> list[Server]|None:
        """An array of Server Objects, which provide connectivity information to a target server.
        If the servers field is not provided, or is an empty array, the default value would be a Server Object with a url value of /."""
        return [Server(e) for e in self.get('servers', [])]
    @servers.setter
    def servers(self, v:list[Server]|None) -> None:
        if v is None:
            del self['servers']
        else:
            self['servers'] = [e.asDictionary() for e in v]
