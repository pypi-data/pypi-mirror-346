.PHONY: build publish publish_test debug_local debug_pypi

build:
	uv run -m build

publish: 
	uv run twine upload dist/*

publish_test:
	uv run twine upload --repository testpypi dist/*

debug_local:
	npx @modelcontextprotocol/inspector uv run -m tws_drex_mcp

debug_pypi:
	npx @modelcontextprotocol/inspector uvx tws-drex-mcp
