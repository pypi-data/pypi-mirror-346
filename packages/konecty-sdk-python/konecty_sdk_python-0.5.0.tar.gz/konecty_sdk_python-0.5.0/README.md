## Konecty Python SDK

> 🛠️ Work in progress

#### Build & Publish

It is needed to increase the version number on the [pyproject](./pyproject.toml) file.

```sh

uv build
uvx twine upload --config-file .pypirc --skip-existing dist/*

```
