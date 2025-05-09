# SPDX-FileCopyrightText: Copyright (C) Shaun Wilson
# SPDX-License-Identifier: MIT

from typing import Callable
from ..MetaManager import MetaManager


def api(tag:str = None) -> Callable:
    """
    Indicates the ``tag`` of a request method or RequestHandler class.
    
    A ``tag`` is an OpenAPI mechanism to group endpoints logically.

    Can be applied to classes or methods. For example, if you apply it to your ``RequestHandler`` subclass then your RequestHandler subclass will appear in ``swagger-ui`` as its own group of endpoints.

    If no value for ``tag`` is provided and the target is a class, the class name is used. Otherwise the decorator will raise an error.

    If a request method or api is, categorically, part of more than one group this decorator may be applied multiple times to associate with all groups.
    """
    def wrapper(target:Callable) -> Callable:
        nonlocal tag
        if tag is None and hasattr(target, '__class__') and target.__class__.__name__ == 'type':
            tag = target.__name__
        if tag is not None:
            tags = MetaManager.instance().tags.get(target, None)
            if tags is None:
                MetaManager.instance().tags[target] = list[str]([tag])
            else:
                tags.append(tag)
        return target
    return wrapper
