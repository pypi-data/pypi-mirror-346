# SPDX-FileCopyrightText: Copyright (C) Shaun Wilson
# SPDX-License-Identifier: MIT

import enum


class ParameterStyle(enum.StrEnum):
    """In order to support common ways of serializing simple parameters, a set of style values are defined."""
    MATRIX = 'matrix'
    """Path-style parameters defined by RFC6570"""
    LABEL = 'label'
    """Label style parameters defined by RFC6570"""
    SIMPLE = 'simple'
    """Simple style parameters defined by RFC6570. This option replaces collectionFormat with a csv value from OpenAPI 2.0."""
    FORM = 'form'
    """Form style parameters defined by RFC6570. This option replaces collectionFormat with a csv (when explode is false) or multi (when explode is true) value from OpenAPI 2.0."""
    SPACEDELIMITED = 'spaceDelimited'
    """Space separated array values or object properties and values. This option replaces collectionFormat equal to ssv from OpenAPI 2.0."""
    PIPEDELIMITED = 'pipeDelimited'
    """Pipe separated array values or object properties and values. This option replaces collectionFormat equal to pipes from OpenAPI 2.0."""
    DEEPOBJECT = 'deepObject'
    """Allows objects with scalar properties to be represented using form parameters. The representation of array or object properties is not defined."""
