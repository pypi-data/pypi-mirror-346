# SPDX-FileCopyrightText: Copyright (C) Shaun Wilson
# SPDX-License-Identifier: MIT

from typing import Any
from .DescriptionObject import DescriptionObject


class Tag(DescriptionObject):
    """
    A simple object to allow referencing other components in the OpenAPI Description, internally and externally.

    The $ref string value contains a URI RFC3986, which identifies the value being referenced.
    """

    def __init__(self, d:dict[str,Any] = None, ref:str = None, summary:str = None, description:str = None) -> None:
        super().__init__(d)
        if d is None:
            self.ref = ref
            self.summary = summary
            self.description = description

    @property
    def ref(self) -> str:
        """
        REQUIRED. The reference identifier. This MUST be in the form of a URI.
        """
        return self.get('$ref', None)
    @ref.setter
    def ref(self, v:str) -> None:
        self['$ref'] = v

    @property
    def summary(self) -> str|None:
        """A short summary which by default SHOULD override that of the referenced component. If the referenced object-type does not allow a summary field, then this field has no effect."""
        return self.get('summary', None)
    @summary.setter
    def summary(self, v:str|None) -> None:
        if v is None:
            del self['summary']
        else:
            self['summary'] = v

    @property
    def description(self) -> str|None:
        """A description which by default SHOULD override that of the referenced component. CommonMark syntax MAY be used for rich text representation. If the referenced object-type does not allow a description field, then this field has no effect."""
        return self.get('description', None)
    @description.setter
    def description(self, v:str|None) -> None:
        if v is None:
            del self['description']
        else:
            self['description'] = v
