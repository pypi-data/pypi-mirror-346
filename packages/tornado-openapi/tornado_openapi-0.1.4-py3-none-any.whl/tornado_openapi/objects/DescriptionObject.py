# SPDX-FileCopyrightText: Copyright (C) Shaun Wilson
# SPDX-License-Identifier: MIT

from abc import ABC
import json
from typing import Any, ForwardRef


DescriptionObject = ForwardRef('DescriptionObject')
class DescriptionObject(ABC):
    """
    A base class for all "Description Objects" that need to convert to/from dictionary objects internally.

    This because, ultimately, all Description Objects must be serialized to JSON (or YAML) and the easiest way to accomplish this is to pull a ``dict`` object hierarchy.
    """

    __d:dict[str,Any]

    def __init__(self, d:dict[str,Any] = None):
        self.__d = dict[str,Any]() if d is None else {
            k:v if not isinstance(v, DescriptionObject) else v.asDictionary()
            for k,v in d.items()
        }

    def __getitem__(self, key:str) -> Any:
        """Get the value for the given key."""
        result = self.__d.get(key, None)
        return None if result is None else result

    def __setitem__(self, key:str, value:Any) -> None:
        """Set the item to the given value. If ``value`` is ``None`` delete the item."""
        self.set(key, value)

    def __delitem__(self, key:str) -> None:
        """Delete the item."""
        self.pop(key)

    def __str__(self) -> str:
        """Serialize complex type as JSON."""
        try:
            return json.dumps(self.__d)
        except:
            return type(self)
            
    def asDictionary(self) -> dict[str,Any]:
        """Returns the backing dictionary object as-is."""
        return self.__d

    def clear(self) -> None:
        """Removes all items from the object."""
        self.__d.clear()

    def get(self, key:str, default:Any = None) -> Any:
        """Gets the value for the given key."""
        v = self.__d.get(key, None)
        return default if v is None else v

    def merge(self, other:DescriptionObject|dict) -> Any:
        """
        Merges the contents of another :py:class:`~tornado_openapi.objects.DescriptionObject` (or dictionary) into the current instance.

        :param DescriptionObject|dict other: The "other" object to merge.
        
        """
        if isinstance(other, DescriptionObject):
            # extract underlying dictionary
            other = other.asDictionary()
        # replace or update
        self.__d.update(other)
        return self

    def pop(self, key:str, default:Any = None) -> Any|None:
        """Delete the item, returning its value. If the item does not exist ``default`` is returned."""
        return self.__d.pop(key, default)

    def set(self, key:str, value:DescriptionObject|None = None) -> None:
        """Sets a value for the given key."""
        if value is None:
            self.pop(key)
        elif isinstance(value, DescriptionObject):
            self.__d[key] = value.asDictionary()
        else:
            self.__d[key] = value
