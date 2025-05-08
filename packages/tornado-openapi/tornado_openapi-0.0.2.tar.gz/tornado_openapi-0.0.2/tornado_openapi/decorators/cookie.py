# SPDX-FileCopyrightText: Copyright (C) Shaun Wilson
# SPDX-License-Identifier: MIT

from typing import Callable

from ..MetaManager import MetaManager
from ..objects.Parameter import Parameter
from ..objects.ParameterLocation import ParameterLocation


def cookie(name:str, t:type = str, description:str = None, required:bool = False, deprecated:bool = False) -> Callable:
    """
    Indicates that a request handler expects a cookie.

    :param str name: REQUIRED. The cookie name that is expected.
    :param type t: If the cookie represents a particular data type. Encoding/Decoding the cookie remains the responsibility of the application/server. Default is `str`.
    :param str description: An optional description for the header or its content.
    :param bool required: `True` If the cookie is required. Default is `False`.
    :param bool deprecated: `True` If the cookie is deprecated. Default is `False`.
    """
    def wrapper(target:Callable) -> Callable:
        cookies = MetaManager.instance().cookies.get(target, None)
        if cookies is None:
            cookies = dict[str, Parameter]()
            MetaManager.instance().cookies[target] = cookies
        cookie = cookies.get(name, None)
        if cookie is not None:
            raise Exception(f'Multiple definitions for "{name}" on "{target.__name__}".')
        cookie = Parameter()
        cookie.name = name
        cookie.location = ParameterLocation.COOKIE
        cookie.description = description
        cookie.required = True if required == True else None
        cookie.deprecated = True if deprecated == True else None
        cookie.schema = MetaManager.instance().getSchemaForType(t)
        cookies[name] = cookie
        return target
    return wrapper
