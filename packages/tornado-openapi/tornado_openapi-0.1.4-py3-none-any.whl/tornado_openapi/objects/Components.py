# SPDX-FileCopyrightText: Copyright (C) Shaun Wilson
# SPDX-License-Identifier: MIT

from typing import Any
from .DescriptionObject import DescriptionObject
from .Callback import Callback
from .Example import Example
from .Header import Header
from .Link import Link
from .Parameter import Parameter
from .PathItem import PathItem
from .Reference import Reference
from .Response import Response
from .RequestBody import RequestBody
from .Schema import Schema
from .SecurityScheme import SecurityScheme


class Components(DescriptionObject):
    """Holds a set of reusable objects for different aspects of the OAS. All objects defined within the Components Object will have no effect on the API unless they are explicitly referenced from outside the Components Object."""

    def __init__(self, d:dict[str,Any] = None, schemas:dict[str, Schema] = None, responses:dict[str, Response|Reference] = None, parameters:dict[str, Parameter|Reference] = None, examples:dict[str, Example|Reference] = None, requestBodies:dict[str, RequestBody|Reference] = None, headers:dict[str, Header|Reference] = None, securitySchemes:dict[str, SecurityScheme|Reference] = None, links:dict[str, Link|Reference] = None, callbacks:dict[str, Callback|Reference] = None, pathItems:dict[str, PathItem] = None) -> None:
        super().__init__(d)
        if d is None:
            self.schemas = schemas
            self.responses = responses
            self.parameters = parameters
            self.examples = examples
            self.requestBodies = requestBodies
            self.headers = headers
            self.securitySchemes = securitySchemes
            self.links = links
            self.callbacks = callbacks
            self.pathItems = pathItems

    @property
    def schemas(self) -> dict[str, Schema]|None:
        """An object to hold reusable Schema Objects."""
        m = self.get('schemas', None)
        return None if m is None else {
                k:Schema(v)
                for k,v in m.items()
            }
    @schemas.setter
    def schemas(self, m:dict[str, Schema]|None) -> None:
        if m is None:
            del self['schemas']
        else:
            self['schemas'] = {
                k:(v if isinstance(v, dict) else v.asDictionary())
                for k,v in m.items()
            }

    @property
    def responses(self) -> dict[str, Response|Reference]|None:
        """An object to hold reusable Response Objects."""
        m = self.get('responses', None)
        return None if m is None else {
                k:Response(v) if '$ref' not in v else Reference(v)
                for k,v in m.items()
            }
    @responses.setter
    def responses(self, m:dict[str, Response|Reference]|None) -> None:
        if m is None:
            del self['responses']
        else:
            self['responses'] = {
                k:v.asDictionary()
                for k,v in m.items()
            }

    @property
    def parameters(self) -> dict[str, Parameter|Reference]|None:
        """An object to hold reusable Parameter Objects."""
        m = self.get('parameters', None)
        return None if m is None else {
                k:Parameter(v) if '$ref' not in v else Reference(v)
                for k,v in m.items()
            }
    @parameters.setter
    def parameters(self, m:dict[str, Parameter|Reference]|None) -> None:
        if m is None:
            del self['parameters']
        else:
            self['parameters'] = {
                k:v.asDictionary()
                for k,v in m.items()
            }

    @property
    def examples(self) -> dict[str, Example|Reference]|None:
        """An object to hold reusable Example Objects."""
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
    def requestBodies(self) -> dict[str, RequestBody|Reference]|None:
        """An object to hold reusable Request Body Objects."""
        m = self.get('requestBodies', None)
        return None if m is None else {
                k:RequestBody(v) if '$ref' not in v else Reference(v)
                for k,v in m.items()
            }
    @requestBodies.setter
    def requestBodies(self, m:dict[str, RequestBody|Reference]|None) -> None:
        if m is None:
            del self['requestBodies']
        else:
            self['requestBodies'] = {
                k:v.asDictionary()
                for k,v in m.items()
            }

    @property
    def headers(self) -> dict[str, Header|Reference]|None:
        """An object to hold reusable Header Objects."""
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
    def securitySchemes(self) -> dict[str, SecurityScheme|Reference]|None:
        """An object to hold reusable Security Scheme Objects."""
        m = self.get('securitySchemes', None)
        return None if m is None else {
                k:SecurityScheme(v) if '$ref' not in v else Reference(v)
                for k,v in m.items()
            }
    @securitySchemes.setter
    def securitySchemes(self, m:dict[str, SecurityScheme|Reference]|None) -> None:
        if m is None:
            del self['securitySchemes']
        else:
            self['securitySchemes'] = {
                k:v.asDictionary()
                for k,v in m.items()
            }

    @property
    def links(self) -> dict[str, Link|Reference]|None:
        """An object to hold reusable Link Objects."""
        m = self.get('links', None)
        return None if m is None else {
                k:Link(v) if '$ref' not in v else Reference(v)
                for k,v in m.items()
            }
    @links.setter
    def links(self, m:dict[str, Link|Reference]|None) -> None:
        if m is None:
            del self['links']
        else:
            self['links'] = {
                k:v.asDictionary()
                for k,v in m.items()
            }

    @property
    def callbacks(self) -> dict[str, Callback|Reference]|None:
        """An object to hold reusable Callback Objects."""
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
    def pathItems(self) -> dict[str, PathItem]|None:
        """An object to hold reusable Path Item Objects."""
        m = self.get('pathItems', None)
        return None if m is None else {
                k:PathItem(v)
                for k,v in m.items()
            }
    @pathItems.setter
    def pathItems(self, m:dict[str, PathItem]|None) -> None:
        if m is None:
            del self['pathItems']
        else:
            self['pathItems'] = {
                k:v.asDictionary()
                for k,v in m.items()
            }
