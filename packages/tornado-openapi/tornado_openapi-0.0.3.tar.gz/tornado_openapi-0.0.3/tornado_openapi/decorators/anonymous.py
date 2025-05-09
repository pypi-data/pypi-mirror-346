# SPDX-FileCopyrightText: Copyright (C) Shaun Wilson
# SPDX-License-Identifier: MIT

from typing import Callable

from ..MetaManager import MetaManager
from ..objects.SecurityRequirement import SecurityRequirement


def anonymous(target:Callable) -> Callable:
    """
    Indicates that a request handler, or request handler method, should not require authentication.
    """
    security = MetaManager.instance().security.get(target, None)
    if security is None:
        security = list[SecurityRequirement]()
        MetaManager.instance().security[target] = security
    # intentionally adding an empty security requirement as an override to allow anonymous access
    security.append(SecurityRequirement())
    return target
