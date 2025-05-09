# SPDX-FileCopyrightText: Copyright (C) Shaun Wilson
# SPDX-License-Identifier: MIT

from typing import Callable

from .objects.Info import Info
from .objects.SecurityScheme import SecurityScheme


class OpenApiConfiguration:
    """
    The configuration to be used when generating an OAS document.
    """
    disableSchemaNamespaces:bool
    """An override option to disable schema namespacing. Can result in collisions, should be used with caution. Default is ``False``."""
    filter:Callable[[str], bool]
    """A callback/predicate function to filter ``tag`` content. Useful for separating OAS by API Version, or similar, where you want to have two OAS endpoints, two configurations, and then need to filter which tags/APIs appear in each OAS. Default is ``lambda e: True``."""
    info:Info
    """The Info Object to be used when describing the API. Default is ``None``."""
    pattern:str
    """The path match pattern to be used with Tornado for serving OAS documents and (when installed) ``swagger-ui``. Default is ``r'/(swagger.*)'``."""
    securitySchemes:dict[str,SecurityScheme]
    """The Security Schema Objects defined for the the API. Default is ``None``."""
    staticFilesPath:str
    """The static files path where ``swagger-ui`` can be found. Default is ``./swagger-ui``."""
