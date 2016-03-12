help:
	@echo "  env         create a development environment using virtualenv"
	@echo "  deps        install dependencies"
	@echo "  clean       remove unwanted stuff"
	@echo "  coverage    run tests with code coverage"
	@echo "  test        run tests"

env_pre:
	pip install virtualenv

env_post:
	. env/bin/activate && \
	make deps

env2: clean
	make env_pre
	virtualenv -p python2.7 env
	make env_post

env3: clean
	make env_pre
	virtualenv -p python3 env
	make env_post

deps:
	pip install -r requirements.txt

clean:
	rm -rf build
	rm -rf dist
	rm -rf env
	rm -rf targetprocess_client.egg-info
	find . -name '*.pyc' -exec rm -f {} \;

coverage:
	coverage run --omit=tests -m unittest discover

test:
	python -m unittest discover

build: clean
	python setup.py sdist
	python setup.py bdist_wheel

upload: clean
	python setup.py sdist upload -r pypi
	python setup.py bdist_wheel upload -r pypi
