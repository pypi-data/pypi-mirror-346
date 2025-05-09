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
    filter:Callable[[str], bool]
    info:Info
    pattern:str
    securitySchemes:dict[str,SecurityScheme]
    staticFilesPath:str
