# SPDX-FileCopyrightText: Copyright (C) Shaun Wilson
# SPDX-License-Identifier: MIT

from typing import Callable

from ..MetaManager import MetaManager
from ..objects.Parameter import Parameter
from ..objects.ParameterLocation import ParameterLocation


def header(name:str, t:type = str, description:str = None, required:bool = False, deprecated:bool = False) -> Callable:
    """
    Indicates that a request handler expects a particular header.

    :param str name: REQUIRED. The header name that is expected.
    :param type t: If the header represents a particular data type. Encoding/Decoding the header remains the responsibility of the application/server. Default is ``str``.
    :param str description: An optional description for the header or its content.
    :param bool required: ``True`` If the header is required. Default is ``False``.
    :param bool deprecated: ``True`` If the header is deprecated. Default is ``False``.
    """
    def wrapper(target:Callable) -> Callable:
        headers = MetaManager.instance().headers.get(target, None)
        if headers is None:
            headers = dict[str, Parameter]()
            MetaManager.instance().headers[target] = headers
        header = headers.get(name, None)
        if header is not None:
            raise Exception(f'Multiple definitions for "{name}" on "{target.__name__}".')
        header = Parameter()
        header.name = name
        header.location = ParameterLocation.HEADER
        header.description = description
        header.required = True if required == True else None
        header.deprecated = True if deprecated == True else None
        header.schema = MetaManager.instance().getSchemaForType(t)
        headers[name] = header
        return target
    return wrapper
