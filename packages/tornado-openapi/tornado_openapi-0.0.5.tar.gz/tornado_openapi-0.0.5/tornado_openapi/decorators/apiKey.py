# SPDX-FileCopyrightText: Copyright (C) Shaun Wilson
# SPDX-License-Identifier: MIT

from typing import Callable

from ..MetaManager import MetaManager
from ..objects.SecurityRequirement import SecurityRequirement


def apiKey(target:Callable) -> Callable:
    """
    Indicates that API KEY Auth is required.
    """
    security = MetaManager.instance().security.get(target, None)
    if security is None:
        security = list[SecurityRequirement]()
        MetaManager.instance().security[target] = security
    security.append(SecurityRequirement({
        'apiKey':[]
    }))
    return target
