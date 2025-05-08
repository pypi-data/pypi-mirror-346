`tornado-openapi` is an OAS-generation library for [Tornado](https://www.tornadoweb.org).

This README is only a high-level introduction to **tornado-openapi**. For more detailed documentation, please view the official docs at [https://tornado-openapi.readthedocs.io](https://tornado-openapi.readthedocs.io).

## Installation

You can install `tornado-openapi` from [PyPI](https://pypi.org/project/tornado-openapi) through usual means, such as `pip`:

```bash
pip install tornado-openapi
```

## Quick Start

For the broadest support, your tornado entry should have a regex which resolves `swagger` files.

Consider this naive example:

```python
import tornado_openapi as openapi
import tornado.web

tornado.web.Application([
    (r'/(swagger.*)', openapi.OpenApiHandler)
])
```

Or, if you prefer something more constrained:

```python
tornado.web.Application([
    (r'/swagger/(.*)', openapi.OpenApiHandler)
])
```

These path matches ensure that `OpenApiHandler` is able to accept and handle
swagger document requests. By default OpenApiHandler will serve `swagger-ui`
if no document name is provided. If you specify "swagger.json" in
the uri the handler will instead generate a schema document (as opposed
to serving `swagger-ui`.)

## Wait, where is `swagger-ui` ?

Alas, `swagger-ui` is NOT included as part of the `tornado-openapi` library. The reasons, in order of importance:

* We do not want to thrust a specific version of `swagger-ui` upon anyone. You may already have a version rolled into your front-end project, for example. You may want a version that is newer than what was current at the time the library was last published.
* We do not wish to encounter licensing issues, as `swagger-ui` currently falls under a different license than the licenses we typically publish under.
* We want to keep our packages small. Storage costs money, networks get congested, and small packages are great for keeping CI/CD times low.
* Indeed, we could rely on a CDN, but some enterprise security audits will identify a third-party CDN as a potential threat -- and again, we do nto want to thrust upon anyone a specific version of `swagger-ui`.

Worry not, by default `tornado-openapi` will serve `swagger-ui` out of the relative path `./swagger-ui/` if it is present. It will assume the contents are a "swagger-ui-dist" bundle, and it will assume the default document is "index.html". You can, of course, customize this by passing the relevant path information into `OpenApiHandler`.

Whether or not `swagger-ui` is installed the `OpenApiHandler` will still generate a schema whenever `swagger.json` is requested. This ensures that integrations (too many to list here, from "cloud gateways" to "dev/test tools") can still be pointed at your server to acquire the necessary schema details of your APIs.

If you are a developer, build engineer, or operator and you wish to slip `swagger-ui` into the build artifacts of your product you can acquire "swagger-ui-dist" which is a self-contained `swagger-ui` distribution. The simplest approach would be to pull [the git repo](https://github.com/swagger-api/swagger-ui/) using `git`, then move/copy the `dist` directory or its contents into the `./swagger-ui` directory of your build output. This avoids a dependency on `npm` tooling, ensures you can have a fresh version of `swagger-ui`. Example:

```bash

# NOTE: remove `--branch v5.21.0` to pull latest from `master`, or, change the version to any valid tag to pull that version.
rm -rf ./swagger-ui && \
rm -rf /tmp/swagger-ui-repo && \
git clone --depth 1 --branch v5.21.0 https://github.com/swagger-api/swagger-ui.git /tmp/swagger-ui-repo && \
cp -r /tmp/swagger-ui-repo/dist ./swagger-ui && \
cp -r /tmp/swagger-ui-repo/LICENSE ./swagger-ui/LICENSE && \
cp -r /tmp/swagger-ui-repo/NOTICE ./swagger-ui/NOTICE && \
rm -rf /tmp/swagger-ui-repo
# if you want to slim down the dist to only what you need:
rm -f ./swagger-ui/*-bundle-*
rm -f ./swagger-ui/*-es-*
rm -f ./swagger-ui/*.map

```

The relative pathing and decision to use `/tmp` are highly dependent on your build environment and security practices, I leave the obvious decisions up to you and your peers.

If you have an existing front-end with `swagger-ui` installed as a package (via `npm`) simply configure the relevant `swagger.json` url you've defined in tornado and everything should work as intended. I defer to [the official documentation](https://swagger.io/tools/swagger-ui/) for configuring and using `swagger-ui`.

Lastly, you can customize the static files path of `swagger-ui` and the url of `swagger.json` by passing in additional intializer params:

```python
(r'/(swagger.*)', openapi.OpenApiHandler, { swaggerStaticFiles='/path/to/swagger-ui', swaggerJsonUrl='/swagger/swagger.json' })
```

Enjoy!


## Contact

You can reach me on [Discord](https://discordapp.com/users/307684202080501761) or [open an Issue on Github](https://github.com/wilson0x4d/tornado_openapi/issues/new/choose).
