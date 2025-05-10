# SPDX-FileCopyrightText: Copyright (C) Shaun Wilson
# SPDX-License-Identifier: MIT

from typing import Any
from .DescriptionObject import DescriptionObject
from .OAuthFlow import OAuthFlow


class OAuthFlows(DescriptionObject):
    """Allows configuration of the supported OAuth Flows."""

    def __init__(self, d:dict[str,Any] = None, implicit:OAuthFlow = None, password:OAuthFlow = None, clientCredentials:OAuthFlow = None, authorizationCode:OAuthFlow = None) -> None:
        super().__init__(d)
        if d is None:
            self.implicit = implicit
            self.password = password
            self.clientCredentials = clientCredentials
            self.authorizationCode = authorizationCode

    @property
    def implicit(self) -> OAuthFlow|None:
        """Configuration for the OAuth Implicit flow."""
        v = self.get('implicit', None)
        return None if v is None else OAuthFlow(v)
    @implicit.setter
    def implicit(self, v:OAuthFlow|None) -> None:
        if v is None:
            del self['implicit']
        else:
            self['implicit'] = v.asDictionary()

    @property
    def password(self) -> OAuthFlow|None:
        """Configuration for the OAuth Resource Owner Password flow."""
        v = self.get('password', None)
        return None if v is None else OAuthFlow(v)
    @password.setter
    def password(self, v:OAuthFlow|None) -> None:
        if v is None:
            del self['password']
        else:
            self['password'] = v

    @property
    def clientCredentials(self) -> OAuthFlow|None:
        """Configuration for the OAuth Client Credentials flow. Previously called application in OpenAPI 2.0."""
        v = self.get('clientCredentials', None)
        return None if v is None else OAuthFlow(v)
    @clientCredentials.setter
    def clientCredentials(self, v:OAuthFlow|None) -> None:
        if v is None:
            del self['clientCredentials']
        else:
            self['clientCredentials'] = v.asDictionary()

    @property
    def authorizationCode(self) -> OAuthFlow|None:
        """Configuration for the OAuth Authorization Code flow. Previously called accessCode in OpenAPI 2.0."""
        v = self.get('authorizationCode', None)
        return None if v is None else OAuthFlow(v)
    @authorizationCode.setter
    def authorizationCode(self, v:OAuthFlow|None) -> None:
        if v is None:
            del self['authorizationCode']
        else:
            self['authorizationCode'] = v.asDictionary()
