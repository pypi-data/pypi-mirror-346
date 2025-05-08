# mijin-openapi-python-client

## generate

カレントディレクトリで実行

```sh
uv run openapi-generator-cli generate \
  -i ../openapi3.yml \
  -g python \
  -o . \
  -c openapi_config.json
```
