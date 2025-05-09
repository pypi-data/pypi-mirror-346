# SPDX-FileCopyrightText: Copyright (C) Shaun Wilson
# SPDX-License-Identifier: MIT

from typing import Callable

from ..MetaManager import MetaManager
from ..objects.Header import Header
from ..objects.MediaType import MediaType
from ..objects.Responses import Responses
from ..objects.Response import Response


def response(code:int|str, t:type = None, contentType:str = 'application/json', description:str = None, headers:dict[str,Header|type] = None) -> Callable:
    """
    Indicates a potential response of a request handler method. A response definition may or may not define a response payload using `t` and `contentType`.

    :param int code: REQUIRED. An HTTP Status Code, such as `200`, or `429`.
    :param type t: If a payload should be expected in the response, this indicates the type of the payload to expect.
    :param str contentType: If a response payload is expected, this indicates the Content-Type of that payload. Default is `"application/json"`.
    :param str description: An optional description for the expected content.
    """
    if type(code) is int:
        code = str(code)
    def wrapper(target:Callable) -> Callable:
        responses = MetaManager.instance().responses.get(target, None)
        if responses is None:
            responses = Responses()
            MetaManager.instance().responses[target] = responses
        response = responses.get(code, None)
        if response is None:
            response = Response(
                description=description,
                content={}
            )
        if t is not None:
            content = response.content
            mt = content.get(contentType, None)
            if mt is not None:
                raise Exception(f'Multiple definitions for "{contentType}" on "{target.__name__}".')
            else:
                content[contentType] = MediaType(
                    schema=MetaManager.instance().getSchemaForType(t)
                )
            response.content = content
        # headers
        if headers is not None and len(headers) > 0:
            response.headers = {
                k:v if isinstance(v,Header) else Header(schema=MetaManager.instance().getSchemaForType(v))
                for k,v in headers.items()
            }
        # TODO: links?
        responses[code] = response
        return target
    return wrapper
