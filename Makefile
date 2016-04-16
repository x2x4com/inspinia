PIP_INDEX_URL = https://pypi.python.org/simple

project_dir := $(realpath $(dir $(lastword $(MAKEFILE_LIST))))

egg_info_tag_build := $(TRAVIS_BUILD_NUMBER)
ifeq ($(egg_info_tag_build),)
egg_info_tag_build := dev
endif

ifeq ($(VIRTUAL_ENV)$(CONDA_ENV_PATH),)
$(error must run in a virtualenv)
else
$(info running in virtualenv $(VIRTUAL_ENV)$(CONDA_ENV_PATH))
endif

# find project python source dirs
initpys := $(foreach dir,$(wildcard $(project_dir)/*),$(wildcard $(dir)/__init__.py))
python_source_dirs := $(foreach initpy,$(initpys),$(realpath $(dir $(initpy))))
$(info found python source in $(python_source_dirs))

.PHONY: all init install check lint test test-unit test-integration build clean

all: init install check build

init:
	pip install -i $(PIP_INDEX_URL) -U setuptools
	pip install -i $(PIP_INDEX_URL) -U pip
	pip install -i $(PIP_INDEX_URL) -U pip-tools

install: requirements.txt
	pip-sync -i $(PIP_INDEX_URL)

PIP_COMPILE_UPGRADE ?= 0
ifneq ($(PIP_COMPILE_UPGRADE),0)
pip_compile_flags += --upgrade
endif
pip_compile = pip-compile -i $(PIP_INDEX_URL) $(pip_compile_flags)

requirements.txt: requirements.in install-requirements.txt
	$(pip_compile) requirements.in

install-requirements.txt: install-requirements.in
	$(pip_compile) install-requirements.in

check: lint test

lint:
	PYTHONPATH=$(project_dir) pylint --rcfile=$(project_dir)/pylintrc --reports=n $(python_source_dirs)

pytest := PYTHONPATH=$(project_dir) py.test -v -l --doctest-modules$(foreach dir,$(python_source_dirs), --ignore="$(dir)/migrations/")
pytest_targets := $(project_dir)/tests/ $(python_source_dirs)

test:
	$(pytest)$(foreach dir,$(python_source_dirs), --cov="$(dir)") --cov-report=term-missing $(pytest_targets)

test-unit:
	$(pytest) -m "not integration" $(pytest_targets)

test-integration:
	$(pytest) -k "not migrations" -m integration $(pytest_targets)

build:
	python setup.py egg_info --tag-build=.$(egg_info_tag_build) bdist_wheel --python-tag py27

clean:
	find $(project_dir) -name '*.pyc' -print -exec rm -r -- {} +
	find $(project_dir) -name '__pycache__' -print -exec rm -r -- {} +
	find $(project_dir) -name '.cache' -print -exec rm -r -- {} +
	find $(project_dir) -name '*.egg-info' -print -exec rm -r -- {} +
	rm -fv $(project_dir)/.coverage
	rm -rfv $(project_dir)/build
	rm -rfv $(project_dir)/dist
