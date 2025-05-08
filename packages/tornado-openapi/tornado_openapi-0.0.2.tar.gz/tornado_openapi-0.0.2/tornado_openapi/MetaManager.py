# SPDX-FileCopyrightText: Copyright (C) Shaun Wilson
# SPDX-License-Identifier: MIT

from datetime import datetime, timezone
import inspect
import math
from typing import Any
from uuid import uuid4

from .objects.Parameter import Parameter
from .objects.Reference import Reference
from .objects.Responses import Responses
from .objects.RequestBody import RequestBody
from .objects.Schema import Schema
from .objects.SecurityRequirement import SecurityRequirement

_wellKnownTypeSchemas:dict[str,Schema] = {
    'Any': Schema().merge(dict(
        type='any'
    )),
    'object': Schema().merge(dict(
        type='any'
    )),
    'int': Schema().merge(dict(
        type='number',
        example=42
    )),
    'str': Schema().merge(dict(
        type='string'
    )),
    'float': Schema().merge(dict(
        type='number',
        example=math.pi
    )),
    'complex': Schema().merge(dict(
        type='string',
        example="string"
    )),
    'bool': Schema().merge(dict(
        type='boolean',
        example=True
    )),
    'UUID': Schema().merge(dict(
        type='str',
        format='uuid',
        example=str(uuid4())
    )),
    'datetime': Schema().merge(dict(
        type='string',
        format='date-time',
        example=datetime.now(tz=timezone.utc).replace(tzinfo=None).isoformat().replace('+00:00', 'Z')
    )),
    'date': Schema().merge(dict(
        type='string',
        format='date',
        example=datetime.now(tz=timezone.utc).replace(tzinfo=None).date().isoformat()
    )),
}


type MetaManager = MetaManager
class MetaManager:

    __security:dict[Any,list[SecurityRequirement]]
    __cookies:dict[Any,dict[str,Parameter]]
    __headers:dict[Any,dict[str,Parameter]]
    __instance:MetaManager = None
    __responses:dict[Any,Responses]
    __requests:dict[Any,RequestBody]
    __schemas:dict[str,Schema]
    __tags:dict[Any,str]

    def __init__(self):
        self.__security = dict[Any,list[SecurityRequirement]]()
        self.__cookies = dict[Any,dict[str,Parameter]]()
        self.__headers = dict[Any,dict[str,Parameter]]()
        self.__responses = dict[Any,Responses]()
        self.__requests = dict[Any,RequestBody]()
        self.__schemas = dict[str,Schema]()
        self.__schemas.update(_wellKnownTypeSchemas)
        self.__tags = dict[Any,str]()

    @property
    def security(self) -> dict[Any,list[SecurityRequirement]]:
        return self.__security

    @property
    def cookies(self) -> dict[Any,dict[str,Parameter]]:
        return self.__cookies

    @property
    def headers(self) -> dict[Any,dict[str,Parameter]]:
        return self.__headers

    @property
    def responses(self) -> dict[Any,Responses]:
        return self.__responses

    @property
    def requests(self) -> dict[Any,RequestBody]:
        return self.__requests

    @property
    def schemas(self) -> dict[str,Schema]:
        return self.__schemas

    @property
    def tags(self) -> dict[Any,list[str]]:
        return self.__tags

    @classmethod
    def instance(cls) -> MetaManager:
        if cls.__instance is None:
            cls.__instance = MetaManager()
        return cls.__instance

    def __getSchemaRefForType(self, t:type) -> str:
        wellKnown = _wellKnownTypeSchemas.get(t.__name__, None)
        if wellKnown is not None:
            return t.__name__
        elif t.__name__ == 'list' and t.__module__ == 'builtins':
            return 'list'
        elif t.__name__ == 'dict' and t.__module__ == 'builtins':
            # TODO: no better way?
            return 'dict'
        elif t.__name__ == 'tuple' and t.__module__ == 'builtins':
            # TODO: no better way?
            return 'tuple'
        elif t.__module__.endswith(f'.{t.__name__}'):
            return f'#/components/schemas/{t.__module__}'
        else:
            return f'#/components/schemas/{t.__module__}.{t.__name__}'

    def getSchemaForType(self, t:type) -> Schema|Reference:
        schemaRef:str = self.__getSchemaRefForType(t if t is not None else Any)
        schema:Schema = MetaManager.instance().schemas.get(schemaRef, None)
        match schemaRef:
            case 'list':
                if hasattr(t, '__args__'):
                    argSchemaRef = self.__getSchemaRefForType(t.__args__[0])
                    argSchema = MetaManager.instance().schemas.get(argSchemaRef)
                    schema = Schema({
                        'type': 'array',
                        'items': argSchema.asDictionary()
                    })
                else:
                    schema = Schema({
                        'type': 'array',
                        'items': MetaManager.instance().schemas.get('any').asDictionary()
                    })
            case 'dict':
                # NOTE: recheck for dict and emit 'additionalProperties' (or allow 'any' items)
                if hasattr(t, '__args__'):
                    argSchemaRef = self.__getSchemaRefForType(t.__args__[1])
                    argSchema = MetaManager.instance().schemas.get(argSchemaRef)
                    schema = Schema({
                        'type': 'object',
                        'additionalProperties': argSchema.asDictionary()
                    })
                else:
                    schema = Schema({
                        'type': 'object',
                        'items': MetaManager.instance().schemas.get('any').asDictionary()
                    })
            case 'tuple':
                if hasattr(t, '__args__'):
                    # typed elements
                    schema = Schema({
                        'type': 'array',
                        'prefixItems': [
                            MetaManager.instance().schemas.get(self.__getSchemaRefForType(arg)).asDictionary()
                            for arg in t.__args__                        
                        ],
                        'minItems': len(t.__args__),
                        'maxItems': len(t.__args__)
                    })
                else:
                    # untyped elements
                    schema = Schema({
                        'type': 'array',
                        'items': MetaManager.instance().schemas.get('any').asDictionary(),
                        'minItems': len(t.__args__),
                        'maxItems': len(t.__args__)
                    })
            case _:
                # all other cases, schema is an object
                if schema is None:
                    schema = Schema()
                    # NOTE: stored up front to prevent cycles for self-referencing type definitions
                    MetaManager.instance().schemas[schemaRef] = schema
                    schema['type'] = 'object'
                    schema['properties'] = dict[str, dict[str,str]]()
                    typeMembers = [(k,v) for k,v in inspect.get_annotations(t).items()]
                    for memberName, memberType in typeMembers:
                        if memberType is None:
                            schema['properties'][memberName] = {
                                'type': 'any'
                            }
                        else:
                            memberSchema = self.getSchemaForType(memberType)
                            schema['properties'][memberName] = memberSchema.asDictionary()
                    # NOTE: assigning a second time to update the schema entry
                    #MetaManager.instance().schemas[schemaRef] = schema
        # conditionally, provide a Reference Object for any type that is not "well-known"
        if schemaRef.startswith('#'):
            return Reference(
                ref=schemaRef
            )
        else:
            return schema

    def getEncoding(self, encoding:str) -> None:
        if encoding is not None:
            raise NotImplementedError('TBD')
        return None
