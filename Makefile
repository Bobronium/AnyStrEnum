VENV_NAME := venv
PYTHON := $(VENV_NAME)/bin/python
VERSION := $(shell $(PYTHON) -c "import anystrenum;print(anystrenum.__version__)")
TEST_PYPI :=  https://test.pypi.org/legacy/

RM := rm -rf

mkvenv:
	dephell venv create

clean:
	find . -name '*.pyc' -exec $(RM) {} +
	find . -name '*.pyo' -exec $(RM) {} +
	find . -name '*~' -exec $(RM)  {} +
	find . -name '__pycache__' -exec $(RM) {} +
	$(RM) build/ dist/ docs/build/ .tox/ .cache/ .pytest_cache/ *.egg-info

convert:
	dephell deps convert --from=pyproject.toml --to setuppy
	dephell deps convert --from=pyproject.toml --to Pipfile

build:
	python3 setup.py sdist bdist_wheel

test:
	dephell project test --env=pytest

upload:
	twine upload dist/*

test-upload:
	twine upload --verbose --repository-url $(TEST_PYPI) dist/*

release:
	make clean
	make test
	make build
	dephell project bump --tag release

fake-release:
	make clean
	dephell project bump release
	make test
	make clean
	dephell project bump pre
	make build
	make test-upload


full-release:
	make release
	make upload
