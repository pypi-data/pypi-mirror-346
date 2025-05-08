# SPDX-FileCopyrightText: Copyright (C) Shaun Wilson
# SPDX-License-Identifier: MIT

from typing import Callable

from ..MetaManager import MetaManager
from ..objects.RequestBody import RequestBody
from ..objects.MediaType import MediaType


def request(t:type, contentType:str = 'application/json', encoding:str = None, description:str = None, required:bool = True) -> Callable:
    """
    Indicates the content that a request handler method expects (aka. "request body")

    :param type t: The Python type that is expected.
    :param str contentType: The content type that is expected.
    :param str encoding: Not Supported, stubbed for future. This is used to indicate an encoding such as multipart mime.
    :param str description: An optional description for the expected content.
    """
    def wrapper(target:Callable) -> Callable:
        if t is not None:
            requestBody = MetaManager.instance().requests.get(target, None)
            if requestBody is None:
                requestBody = RequestBody(
                    description=description,
                    required=required,
                    content={}
                )
                MetaManager.instance().requests[target] = requestBody
            content = requestBody.content
            mt = content.get(contentType, None)
            if mt is not None:
                raise Exception(f'Multiple definitions for "{contentType}" on "{target.__name__}".')
            else:
                content[contentType] = MediaType(
                    schema=MetaManager.instance().getSchemaForType(t),
                    encoding=MetaManager.instance().getEncoding(encoding)
                )
            requestBody.content = content
        return target
    return wrapper
