# SPDX-FileCopyrightText: Copyright (C) Shaun Wilson
# SPDX-License-Identifier: MIT

from typing import Any
from .DescriptionObject import DescriptionObject


class OAuthFlow(DescriptionObject):
    """Configuration details for a supported OAuth Flow."""

    def __init__(self, d:dict[str,Any] = None, authorizationUrl:str = None, tokenUrl:str = None, refreshUrl:str = None, scopes:dict[str,str] = None) -> None:
        super().__init__(d)
        if d is None:
            self.authorizationUrl = authorizationUrl
            self.tokenUrl = tokenUrl
            self.refreshUrl = refreshUrl
            self.scopes = scopes

    @property
    def authorizationUrl(self) -> str|None:
        """REQUIRED FOR ``IMPLCIIT`` OR ``AUTHORIZATIONCODE``. The authorization URL to be used for this flow. This MUST be in the form of a URL. The OAuth2 standard requires the use of TLS."""
        return self.get('authorizationUrl', None)
    @authorizationUrl.setter
    def authorizationUrl(self, v:str|None) -> None:
        if v is None:
            del self['authorizationUrl']
        else:
            self['authorizationUrl'] = v

    @property
    def tokenUrl(self) -> str|None:
        """REQUIRED FOR ``PASSWORD``, ``CLIENTCREDENTIALS``, OR ``AUTHORIZATIONCODE``. The token URL to be used for this flow. This MUST be in the form of a URL. The OAuth2 standard requires the use of TLS."""
        return self.get('tokenUrl', None)
    @tokenUrl.setter
    def tokenUrl(self, v:str|None) -> None:
        if v is None:
            del self['tokenUrl']
        else:
            self['tokenUrl'] = v

    @property
    def refreshUrl(self) -> str|None:
        """The URL to be used for obtaining refresh tokens. This MUST be in the form of a URL. The OAuth2 standard requires the use of TLS."""
        return self.get('refreshUrl', None)
    @refreshUrl.setter
    def refreshUrl(self, v:str|None) -> None:
        if v is None:
            del self['refreshUrl']
        else:
            self['refreshUrl'] = v

    @property
    def scopes(self) -> dict[str,str]|None:
        """REQUIRED. The available scopes for the OAuth2 security scheme. A map between the scope name and a short description for it. The map MAY be empty."""
        return self.get('parameters', None)
    @scopes.setter
    def scopes(self, m:dict[str,str]|None) -> None:
        if m is None:
            del self['scopes']
        else:
            self['scopes'] = m
