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

python_version_full := $(wordlist 2,4,$(subst ., ,$(shell python --version 2>&1)))
python_version_major := $(word 1,${python_version_full})
python_version_minor := $(word 2,${python_version_full})
python_version_patch := $(word 3,${python_version_full})
$(info using python$(python_version_major))

.PHONY: all init install check lint test test-tox test-unit test-integration build clean

all: init install check build

init:
	pip install -i $(PIP_INDEX_URL) -U setuptools
	pip install -i $(PIP_INDEX_URL) -U 'pip<8.1.2'
	pip install -i $(PIP_INDEX_URL) -U pip-tools
	mkdir -p tests/reports

install: requirements-py$(python_version_major).txt
	pip-sync -i $(PIP_INDEX_URL) requirements-py$(python_version_major).txt

PIP_COMPILE_UPGRADE ?= 0
ifneq ($(PIP_COMPILE_UPGRADE),0)
pip_compile_flags += --upgrade
endif
pip_compile = pip-compile -i $(PIP_INDEX_URL) $(pip_compile_flags)

requirements-py2.txt: requirements/python2.in install-requirements-py2.txt
	$(pip_compile) requirements/python2.in -o requirements-py2.txt

install-requirements-py2.txt: requirements/install-python2.in
	$(pip_compile) requirements/install-python2.in -o install-requirements-py2.txt

requirements-py3.txt: requirements/python3.in install-requirements-py3.txt
	$(pip_compile) requirements/python3.in -o requirements-py3.txt

install-requirements-py3.txt: requirements/install-python3.in
	$(pip_compile) requirements/install-python3.in -o install-requirements-py3.txt

check: lint test

lint:
ifeq ($(python_version_major),2)
	PYTHONPATH="$(project_dir)" pylint --rcfile="$(project_dir)/pylintrc" --reports=n $(foreach dir,$(python_source_dirs), "$(dir)")
endif

pytest_args := -v -l$(foreach dir,$(python_source_dirs), --ignore="$(dir)/migrations/")
pytest_cov := $(foreach dir,$(python_source_dirs), --cov="$(dir)") --cov-report=term-missing --cov-report=html --cov-report=xml --no-cov-on-fail
pytest := PYTHONPATH="$(project_dir)" py.test $(pytest_args)
pytest_targets := "$(project_dir)/tests/" $(foreach dir,$(python_source_dirs), "$(dir)")
tox := PYTHONPATH="$(project_dir)" tox

test-tox:
	$(tox) -- $(pytest_args) $(pytest_cov) $(pytest_targets)

test:
	$(pytest) $(pytest_cov) $(pytest_targets)

test-unit:
	$(pytest) -m "not integration" $(pytest_targets)

test-integration:
	$(pytest) -m integration $(pytest_targets)

build:
	python setup.py egg_info --tag-build=+build$(egg_info_tag_build) bdist_wheel --python-tag py27

clean:
	find $(project_dir) -name '*.pyc' -print -exec rm -r -- {} +
	find $(project_dir) -name '__pycache__' -print -exec rm -r -- {} +
	find $(project_dir) -name '.cache' -print -exec rm -r -- {} +
	find $(project_dir) -name '*.egg-info' -print -exec rm -r -- {} +
	rm -rfv $(project_dir)/.tox
	rm -rfv $(project_dir)/.cache
	rm -rfv $(project_dir)/tests/reports
	rm -rfv $(project_dir)/build
	rm -rfv $(project_dir)/dist
