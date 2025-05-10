# SPDX-FileCopyrightText: Copyright (C) Shaun Wilson
# SPDX-License-Identifier: MIT

import enum


class ParameterLocation(enum.StrEnum):
    """There are four possible parameter locations."""
    PATH = 'path'
    """Used together with Path Templating, where the parameter value is actually part of the operation's URL. This does not include the host or base path of the API. For example, in /items/{itemId}, the path parameter is itemId."""
    QUERY = 'query'
    """Parameters that are appended to the URL. For example, in ``/items?id=###``, the query parameter is id."""
    HEADER = 'header'
    """Custom headers that are expected as part of the request. Note that RFC7230 states header names are case insensitive."""
    COOKIE = 'cookie'
    """ Used to pass a specific cookie value to the API."""
