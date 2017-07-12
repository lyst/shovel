.PHONY: help
help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "develop - install dev dependencies and shovel in develop mode"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "sdist - package"

.PHONY: clean
clean: clean-build clean-pyc

.PHONY: clean-build
clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

.PHONY: clean-pyc
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

.PHONY: develop
develop:
	pip install -r dev-requirements.txt

.PHONY: lint
lint:
	.circle/lint-all.sh $${TEST_ARGS:-"src/ tests/"}

.PHONY: test
test:
	- ./.circle/py_tests.sh $${TEST_ARGS:-"tests/"}

.PHONY: coverage
coverage:
	coverage run --source=src/,tests/ --include=src/* -m py.test --strict $${TEST_ARGS:-"tests/"}
	coverage report -m
	coverage html
	open htmlcov/index.html

.PHONY: docs
docs:
	rm -f docs/shovel.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ shovel
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	open docs/_build/html/index.html

.PHONY: release
release: clean
	python setup.py sdist upload
	python setup.py bdist_wheel upload

.PHONY: sdist
sdist: clean
	python setup.py sdist
	python setup.py bdist_wheel upload
	ls -l dist
