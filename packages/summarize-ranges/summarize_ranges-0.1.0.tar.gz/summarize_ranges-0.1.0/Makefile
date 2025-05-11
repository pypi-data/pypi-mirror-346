.PHONY: test clean upload

test:
	uv run pytest

nox:
	uv run nox

clean:
	find . \( -name '*.pyc' -o -name '*~' \) -print0 | xargs -r -0 rm
	find . -name '__pycache__' -type d -print0 | xargs -r -0 rm -r
	find . -name '.pytest_cache' -type d -print0 | xargs -r -0 rm -r
	find . -name '.ruff_cache' -type d -print0 | xargs -r -0 rm -r
	rm -fr build dist

upload:
	uv build
	uv publish $$(ls -t dist/summarize_ranges-*.tar.gz | head -n 1)
