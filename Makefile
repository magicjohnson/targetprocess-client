help:
	@echo "  env         create a development environment using virtualenv"
	@echo "  deps        install dependencies"
	@echo "  clean       remove unwanted stuff"
	@echo "  coverage    run tests with code coverage"
	@echo "  test        run tests"

env:
	pip install virtualenv && \
	virtualenv env && \
	. env/bin/activate && \
	make deps

deps:
	pip install -r requirements.txt

clean:
	rm -rf build
	rm -rf dist
	rm -rf env
	rm -rf targetprocess_client.egg-info
	find . -name '*.pyc' -exec rm -f {} \;

coverage:
	coverage run -m unittest discover

test:
	python -m unittest discover
