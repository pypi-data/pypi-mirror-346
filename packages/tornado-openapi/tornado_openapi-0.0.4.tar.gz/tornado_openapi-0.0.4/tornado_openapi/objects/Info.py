# SPDX-FileCopyrightText: Copyright (C) Shaun Wilson
# SPDX-License-Identifier: MIT

from typing import Any
from .DescriptionObject import DescriptionObject
from .Contact import Contact
from .License import License


class Info(DescriptionObject):
    """
    Provides metadata about the API.
    
    The metadata MAY be used by the clients if needed, and MAY be presented in editing or documentation generation tools for convenience.
    """

    def __init__(self, d:dict[str,Any] = None, title:str = None, summary:str = None, description:str = None, termsOfService:str = None, contact:Contact = None, license:License = None, version:str = None) -> None:
        super().__init__(d)
        if d is None:
            self.title = title
            self.summary = summary
            self.description = description
            self.termsOfService = termsOfService
            self.contact = contact
            self.license = license
            self.version = version

    @property
    def title(self) -> str:
        """REQUIRED. The title of the API."""
        return self.get('title', None)
    @title.setter
    def title(self, v:str) -> None:
        self['title'] = v

    @property
    def summary(self) -> str|None:
        """A short summary of the API."""
        return self.get('summary', None)
    @summary.setter
    def summary(self, v:str|None) -> None:
        if v is None:
            del self['summary']
        else:
            self['summary'] = v

    @property
    def description(self) -> str|None:
        """A description of the API. CommonMark syntax MAY be used for rich text representation."""
        return self.get('description', None)
    @description.setter
    def description(self, v:str|None) -> None:
        if v is None:
            del self['description']
        else:
            self['description'] = v

    @property
    def termsOfService(self) -> str|None:
        """A URI for the Terms of Service for the API. This MUST be in the form of a URI."""
        return self.get('termsOfService', None)
    @termsOfService.setter
    def termsOfService(self, v:str|None) -> None:
        if v is None:
            del self['termsOfService']
        else:
            self['termsOfService'] = v

    @property
    def contact(self) -> Contact|None:
        """The contact information for the exposed API."""
        v = self.get('contact', None)        
        return None if v is None else Contact(v)
    @contact.setter
    def contact(self, v:Contact|None) -> None:
        if v is None:
            del self['contact']
        else:
            self['contact'] = v.asDictionary()

    @property
    def license(self) -> License|None:
        """The license information for the exposed API."""
        v = self.get('license', None)        
        return None if v is None else License(v)
    @license.setter
    def license(self, v:License|None) -> None:
        if v is None:
            del self['license']
        else:
            self['license'] = v.asDictionary()

    @property
    def version(self) -> str:
        """REQUIRED. The version of the OpenAPI Document (which is distinct from the OpenAPI Specification version or the version of the API being described or the version of the OpenAPI Description)."""
        return self.get('version', None)
    @version.setter
    def version(self, v:str) -> None:
        self['version'] = v
