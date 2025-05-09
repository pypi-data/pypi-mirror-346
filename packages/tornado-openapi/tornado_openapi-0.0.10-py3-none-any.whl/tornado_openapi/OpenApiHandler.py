# SPDX-FileCopyrightText: Copyright (C) Shaun Wilson
# SPDX-License-Identifier: MIT

import inspect
import json
import os
import re
from typing import Any
import tornado
import tornado.web

from .MetaManager import MetaManager
from .OpenApiConfiguration import OpenApiConfiguration
from .objects import Components, OpenAPI, Parameter, ParameterLocation, Paths, PathItem, Schema, SecurityRequirement, Operation


class OpenApiHandler(tornado.web.RequestHandler):
    """
    A handler that can return OpenAPI schema docs and ``swagger-ui`` test pages (if installed.)
    """

    __configuration:OpenApiConfiguration
    __requiredSchemas:set[str]
    __swaggerJsonUrl:str

    def __init__(self, application:tornado.web.Application, request:tornado.httputil.HTTPServerRequest, **kwargs) -> None:
        self.__requiredSchemas = set[str]()
        super().__init__(application, request, **kwargs)

    def __resolveTagsFor(self, handler:Any|None = None, action:Any|None = None) -> list[str]|None:
        handlerTags = [] if handler is None else MetaManager.instance().tags.get(handler, [])
        actionTags = [] if action is None else MetaManager.instance().tags.get(action, [])
        tags = handlerTags + actionTags
        return tags
    
    def __getSchemaForParameter(self, oas:OpenAPI, parameter:inspect.Parameter) -> Schema:
        # built-in types (str, int, float, etc)
        schema = MetaManager.instance().getSchemaForType(parameter.annotation)
        return schema
    
    def __tryParameterizePath(self, path:str, positionalParameters:list[str], keywordParameters:list[str], parameters:list[Parameter]) -> tuple[bool, str]:
        """
        Tries to parameterize the path string for the provided parameter names.

        :returns tuple[bool, str]: a tuple containing a bool indicating if parameters could be matched in the path string, and the resulting path string (whether or not parameters matched.)

        ---
        NOTE: Currently, Tornado enforces that all regex captures in a path are either all "named", or all "unnamed", but does not allow a mixture of named and unnamed. This method, however, supports a mixture of named and unnamed.
        """
        # tornado supports named captures.
        #
        # unnamed captures must be matched by position (aka positional args), named captures
        # are mapped to kwargs by tornado.

        # for testing querystring parameters
        def isQueryStringParameter(name:str, parameterizedPath:str) -> bool:
            queryStringDelimiterMatch = re.search(r'[^\(]\?', parameterizedPath)
            if queryStringDelimiterMatch is None:
                return False
            queryStringMinimumPosition = None if queryStringDelimiterMatch is None else queryStringDelimiterMatch.span(0)[1]
            queryStringParameterMatch:re.Match = re.search(name + r'=\{' + name + r'\}', parameterizedPath)
            return queryStringParameterMatch is not None and queryStringParameterMatch.span(0)[0] >= queryStringMinimumPosition

        # replace named/keyword parameters
        result = path
        for name in [e for e in keywordParameters]:
            result, count = re.subn(r'\(\?P\<' + name + r'\>[^\)]+\)', f'{{{name}}}', result)
            if count > 0:
                positionalParameters.remove(name)
                keywordParameters.remove(name)

        # replace unnamed/positional parameters
        def repl(m:re.Match) -> str:
            nonlocal positionalParameters
            if len(positionalParameters) > 0:
                name = positionalParameters[0]
                keywordParameters.remove(name)
                positionalParameters.pop(0)
                return f'{{{name}}}'
            else:
                return m.group(0)

        # finalize            
        result = re.sub(r'\([^\?\)]+\)', repl, result)
        wasSuccessful = len(keywordParameters) == 0 and len(positionalParameters) == 0 and re.search(r'\([^\)]+\)', result) == None
        if wasSuccessful:
            # configure parameters as "querystring" parameters or "path" parameters
            for p in parameters:
                if p.location is None:
                    p.location = ParameterLocation.QUERY if isQueryStringParameter(p.name, result) else ParameterLocation.PATH
        return (wasSuccessful, result)

    def __iterateRules(self, oas:OpenAPI, rules:list[tornado.web.Rule], paths:Paths) -> Paths:
        for rule in rules:
            if isinstance(rule.matcher, tornado.routing.PathMatches):
                m:tornado.routing.PathMatches = rule.matcher
                path = m.regex.pattern.rstrip('$')
                if issubclass(rule.target, tornado.web.RequestHandler):
                    for actionName in ['delete', 'get', 'head', 'options', 'patch', 'post', 'put', 'trace']:
                        action = rule.target.__dict__.get(actionName, None)
                        if action is not None:
                            operation = Operation()
                            # tags
                            tags = self.__resolveTagsFor(rule.target, action)
                            # parameters (args and kwargs)
                            parameters = list[Parameter]()
                            positionalParameterNames = []
                            keywordParameterNames = []
                            signature = inspect.signature(action)
                            for v in signature.parameters.values():
                                if v.name == 'self' or v.name == 'cls':
                                    continue
                                parameter = Parameter()
                                parameter.name = v.name
                                parameter.schema
                                schema = self.__getSchemaForParameter(oas, v)
                                if schema is not None:
                                    parameter.schema = schema
                                    # TODO: support `parameter.style` ?
                                match v.kind:
                                    case inspect._ParameterKind.KEYWORD_ONLY:
                                        keywordParameterNames.append(parameter.name)
                                    case inspect._ParameterKind.POSITIONAL_OR_KEYWORD:
                                        positionalParameterNames.append(parameter.name)
                                        keywordParameterNames.append(parameter.name)
                                    case inspect._ParameterKind.POSITIONAL_ONLY:
                                        positionalParameterNames.append(parameter.name)
                                parameters.append(parameter)

                            # parameters (headers)
                            headers = MetaManager.instance().headers.get(action, None)
                            if headers is not None:
                                for header in headers.values():
                                    parameters.append(header)

                            # parameters (cookies)
                            cookies = MetaManager.instance().cookies.get(action, None)
                            if cookies is not None:
                                for cookie in cookies.values():
                                    parameters.append(cookie)

                            if len(parameters) > 0:
                                operation.parameters = parameters

                            if len(positionalParameterNames) > 0 or len(keywordParameterNames) > 0:
                                # there are params, require matching function to successfully match them all
                                pathMatched, parameterizedPath = self.__tryParameterizePath(path, positionalParameterNames, keywordParameterNames, parameters)
                            elif re.search(r'\([^\)]+\)', path) is None and (len(signature.parameters) == 0 or (len(signature.parameters) == 1 and signature.parameters.get('self', None) is not None)):
                                # there were no params, pseudo a match success (params are not required for an enpoint to invoke)
                                pathMatched = True
                                parameterizedPath = path
                            else:
                                # in this branch the endpoint path contained params, but no params were extracted. this should never happen, but for completeness we pseudo a match failure
                                pathMatched = False
                                parameterizedPath = path

                            # request bodies
                            operation.requestBody = MetaManager.instance().requests.get(action, None)
                            # if operation.requestBody is not None:
                            #     self.__logger.debug(f'no requestBody for {action} on {rule.target.__name__}')

                            # response(s)
                            operation.responses = MetaManager.instance().responses.get(action, None)

                            tags = [t for t in tags if self.__configuration.filter(t)]
                            if pathMatched and tags is not None and len(tags) > 0:
                                # update required schemas (request bodies)
                                if operation.requestBody is not None:
                                    for k,v in operation.requestBody.content.items():
                                        schemaRef = v.schema.get('$ref', None)
                                        if schemaRef is not None:
                                            self.__requiredSchemas.add(schemaRef)
                                # update required schemas (parameters)
                                if operation.parameters is not None:
                                    for p in operation.parameters:
                                        schemaRef = p.get('$ref', None)
                                        if schemaRef is not None:
                                            self.__requiredSchemas.add(schemaRef)
                                # security requirements
                                securityRequirements = MetaManager.instance().security.get(action, None)
                                if securityRequirements is None:
                                    securityRequirements = MetaManager.instance().security.get(rule.target, None)
                                if securityRequirements is not None:
                                    operation.security = securityRequirements
                                operation.tags = tags
                                pathItem = paths[parameterizedPath]
                                if pathItem is None:
                                    pathItem = PathItem()
                                pathItem[actionName] = operation
                                paths[parameterizedPath] = pathItem
            if isinstance(rule.target, tornado.web._ApplicationRouter):
                router:tornado.web._ApplicationRouter = rule.target
                self.__iterateRules(oas, router.rules, paths)
        return paths

    def __buildOpenApiSchema(self) -> OpenAPI:
        oas:OpenAPI = OpenAPI()
        oas.info = self.__configuration.info
 
        # TODO: oas.servers = servers

        # build paths
        oas.paths = self.__iterateRules(oas, self.application.default_router.rules, Paths())
        # build schema dictionary
        components = Components(
            schemas={
                k.replace('#/components/schemas/',''):v
                for k,v in MetaManager.instance().schemas.items()
                # only include non-builtin types (by requiring schema name to start with #)
                if k.startswith('#') and k in self.__requiredSchemas
            },
            securitySchemes=None if self.__configuration.securitySchemes is None or len(self.__configuration.securitySchemes) == 0 else {
                k:v
                for k,v in self.__configuration.securitySchemes.items()
            }
        )
        oas.components = components
        # result
        return oas

    def initialize(self, oaconfig:OpenApiConfiguration, swaggerJsonUrl:str = 'swagger.json') -> None:
        self.__configuration = oaconfig
        self.__swaggerJsonUrl = swaggerJsonUrl

    async def get(self, path:str) -> None:
        if path is None:
            raise tornado.web.HTTPError(500, reason = "Missing URI Path")
        elif path.endswith('.json'):
            # interrogate oas state and serialize to json
            self.set_header('Content-Type', 'application/json')
            result:OpenAPI = self.__buildOpenApiSchema()
            self.write(json.dumps(result.asDictionary()))
            pass
        # elif path.endswith('.yaml'):
        #     # TODO: interrogate oas state and serialize to yaml
        #     self.set_header('Content-Type', 'application/yaml')
        #     # TODO: this should only be performed with `extras` installed, since not everyone will appreciate addt'l dependencies
        #     pass
        else:
            # all other documents will be treated as static resources
            # we strip off any path parts to load `swagger-ui` files directly from disk
            originalPath = path
            targetFile = '' if not '/' in path and not '.' in path else path.split('/')[-1]
            targetFile = 'index.html' if len(targetFile) <= 1 else targetFile
            path = os.path.join(os.path.abspath(self.__configuration.staticFilesPath), targetFile)
            if not os.path.isfile(path):
                raise tornado.web.HTTPError(404)
            else:
                extension = path.split('.')[-1]
                match extension:
                    case 'css':
                        self.set_header('Content-Type', 'text/css')
                    case 'js':
                        self.set_header('Content-Type', 'application/javascript')
                    case 'html':
                        self.set_header('Content-Type', 'text/html')
                with open(path, 'rb') as file:
                    buf = file.read()
                    # rewrite initializer to fetch "our" swagger.json
                    if path.endswith('swagger-initializer.js'):
                        buf = buf.decode()
                        swaggerJsonUrl = self.__swaggerJsonUrl
                        if swaggerJsonUrl.startswith('./'):
                            swaggerJsonUrl = '/' + originalPath.replace(targetFile, '') + swaggerJsonUrl.lstrip('.').lstrip('/')
                        buf = re.sub('url:[^,]+,', f'url:"{swaggerJsonUrl}",', buf)
                    self.write(buf)
                    self.flush()
