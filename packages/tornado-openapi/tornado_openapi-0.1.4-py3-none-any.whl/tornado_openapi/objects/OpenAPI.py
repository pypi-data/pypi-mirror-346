# SPDX-FileCopyrightText: Copyright (C) Shaun Wilson
# SPDX-License-Identifier: MIT

from typing import Any
from .Components import Components
from .DescriptionObject import DescriptionObject
from .Info import Info
from .PathItem import PathItem
from .Paths import Paths
from .SecurityRequirement import SecurityRequirement
from .Server import Server
from .Tag import Tag
from .ExternalDocumentation import ExternalDocumentation


class OpenAPI(DescriptionObject):

    def __init__(self, d:dict[str,Any] = None, openapi:str = '3.1.1', info:Info = None, jsonSchemaDialect:str = None, servers:list[Server] = None, paths:Paths = None, webhooks:dict[str,PathItem] = None, components:Components = None, security:list[SecurityRequirement] = None, tags:list[Tag] = None, externalDocs:ExternalDocumentation = None) -> None:
        super().__init__(d)
        if d is None:
            self.openapi = openapi
            self.info = info
            self.servers = servers
            self.paths = paths
            self.webhooks = webhooks
            self.components = components
            self.security = security
            self.tags = tags
            self.externalDocs = externalDocs

    @property
    def openapi(self) -> str:
        """REQUIRED. This string MUST be the version number of the OpenAPI Specification that the OpenAPI Document uses. The openapi field SHOULD be used by tooling to interpret the OpenAPI Document. This is not related to the API info.version string."""
        return self.get('openapi', None)
    @openapi.setter
    def openapi(self, v:str) -> None:
        self['openapi'] = v

    @property
    def info(self) -> Info:
        """REQUIRED. Provides metadata about the API. The metadata MAY be used by tooling as required."""
        v = self.get('info', None)
        return None if v is None else Info(v)
    @info.setter
    def info(self, v:Info) -> None:
        if v is None:
            self['info'] = {}
        else:
            self['info'] = v.asDictionary()

    @property
    def jsonSchemaDialect(self) -> str|None:
        """The default value for the $schema keyword within Schema Objects contained within this OAS document. This MUST be in the form of a URI."""
        return self.get('jsonSchemaDialect', None)
    @jsonSchemaDialect.setter
    def jsonSchemaDialect(self, v:str|None) -> None:
        if v is None:
            del self['jsonSchemaDialect']
        else:
            self['jsonSchemaDialect'] = v

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

    @property
    def paths(self) -> Paths|None:
        """The available paths and operations for the API."""
        return Paths(self.get('paths', None))
    @paths.setter
    def paths(self, v:Paths|None) -> None:
        if v is None:
            del self['paths']

        else:
            self['paths'] = v.asDictionary()

    @property
    def webhooks(self) -> dict[str, PathItem]|None:
        """The incoming webhooks that MAY be received as part of this API and that the API consumer MAY choose to implement. Closely related to the callbacks feature, this section describes requests initiated other than by an API call, for example by an out of band registration. The key name is a unique string to refer to each webhook, while the (optionally referenced) Path Item Object describes a request that may be initiated by the API provider and the expected responses."""
        m = self.get('webhooks', None)
        return None if m is None else {
                k:PathItem(v)
                for k,v in m.items()
            }
    @webhooks.setter
    def webhooks(self, m:dict[str, PathItem]|None) -> None:
        if m is None:
            del self['webhooks']
        else:
            self['webhooks'] = {
                k:v.asDictionary()
                for k,v in m.items()
            }

    @property
    def components(self) -> Components|None:
        """An element to hold various Objects for the OpenAPI Description."""
        v = self.get('components', None)
        return None if v is None else Components(v)
    @components.setter
    def components(self, v:Components|None) -> None:
        if v is None:
            del self['components']
        else:
            self['components'] = v.asDictionary()

    @property
    def security(self) -> list[SecurityRequirement]|None:
        """A declaration of which security mechanisms can be used across the API.
        The list of values includes alternative Security Requirement Objects that can be used. Only one of the Security Requirement Objects need to be satisfied to authorize a request. Individual operations can override this definition. The list can be incomplete, up to being empty or absent.
        To make security explicitly optional, an empty security requirement (``{}``) can be included in the array."""
        v = self.get('security', None)
        return None if v is None else [SecurityRequirement(e) for e in v]
    @security.setter
    def security(self, v:list[SecurityRequirement]|None) -> None:
        if v is None:
            del self['security']
        else:
            self['security'] = [e.asDictionary() for e in v]


    @property
    def tags(self) -> list[Tag]|None:
        """A list of tags used by the OpenAPI Description with additional metadata. The order of the tags can be used to reflect on their order by the parsing tools. Not all tags that are used by the Operation Object must be declared. The tags that are not declared MAY be organized randomly or based on the tools' logic. Each tag name in the list MUST be unique."""
        return [Tag(e) for e in self.get('tags', None)]
    @tags.setter
    def tags(self, v:list[Tag]|None) -> None:
        if v is None:
            del self['tags']
        else:
            self['tags'] = [e.asDictionary() for e in v]

    @property
    def externalDocs(self) -> ExternalDocumentation|None:
        """Additional external documentation."""
        v = self.get('externalDocs', None)
        return None if v is None else ExternalDocumentation(v)
    @externalDocs.setter
    def externalDocs(self, v:ExternalDocumentation|None) -> None:
        if v is None:
            del self['externalDocs']
        else:
            self['externalDocs'] = v.asDictionary()
