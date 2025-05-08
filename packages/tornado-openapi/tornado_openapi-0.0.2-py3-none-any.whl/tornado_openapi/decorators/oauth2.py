# SPDX-FileCopyrightText: Copyright (C) Shaun Wilson
# SPDX-License-Identifier: MIT

from typing import Callable

from ..MetaManager import MetaManager
from ..objects.SecurityRequirement import SecurityRequirement


def oauth2(scopes:list[str] = []) -> Callable:
    """
    Indicates that OAUTH2 Auth is required.
    """
    def wrapper(target:Callable) -> Callable:
        security = MetaManager.instance().security.get(target, None)
        if security is None:
            security = list[SecurityRequirement]()
            MetaManager.instance().security[target] = security
        security.append(SecurityRequirement({
            'oauth2':scopes
        }))
        return target
    return wrapper
