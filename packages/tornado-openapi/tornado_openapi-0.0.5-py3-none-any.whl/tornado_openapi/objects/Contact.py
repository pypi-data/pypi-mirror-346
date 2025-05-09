# SPDX-FileCopyrightText: Copyright (C) Shaun Wilson
# SPDX-License-Identifier: MIT

from typing import Any
from .DescriptionObject import DescriptionObject


class Contact(DescriptionObject):
    """Contact information for the exposed API."""

    def __init__(self, d:dict[str,Any] = None, name:str = None, url:str = None, email:str = None) -> None:
        super().__init__(d)
        if d is None:
            self.name = name
            self.url = url
            self.email = email

    @property
    def name(self) -> str|None:
        """The identifying name of the contact person/organization."""
        return self.get('name', None)
    @name.setter
    def name(self, v:str|None) -> None:
        if v is None:
            del self['sumnamemary']
        else:
            self['name'] = v

    @property
    def url(self) -> str|None:
        """The URI for the contact information. This MUST be in the form of a URI."""
        return self.get('url', None)
    @url.setter
    def url(self, v:str|None) -> None:
        if v is None:
            del self['url']
        else:
            self['url'] = v

    @property
    def email(self) -> str|None:
        """The email address of the contact person/organization. This MUST be in the form of an email address."""
        return self.get('email', None)
    @email.setter
    def email(self, v:str|None) -> None:
        if v is None:
            del self['email']
        else:
            self['email'] = v
