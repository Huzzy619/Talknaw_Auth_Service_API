PYTHON = .venv/bin/python
PIP = .venv/bin/pip
FLAKE8 = .venv/bin/python -m flake8
BLACK = .venv/bin/python -m black
AUTOFLAKE = .venv/bin/python -m autoflake

venv :
	python3.11 -m venv .venv
	$(PIP) install --upgrade pip
	$(MAKE) install
.PHONY : venv

freeze :
	$(PIP) freeze > constraints.txt
.PHONY : freeze

install :
	$(PIP) install --upgrade pip
	$(PIP) install --index-url "$(PIP_INDEX_URL)" \
		--requirement requirements.txt \
		--constraint constraints.txt
.PHONY : install

clean :
	rm -fr build dist *.egg-info
	rm -fr .pytest_cache .mypy_cache
	rm -fr *.junit.xml .coverage coverage.xml htmlcov
	find . -path ./.venv -prune -o -name __pycache__ -print | xargs rm -fr
.PHONY : clean

clean-venv : clean
	rm -fr .venv
.PHONY : clean-venv

lint : flake8 mypy
flake8 :
	$(FLAKE8) ./auth ./tests
mypy :
	$(MYPY) 
.PHONY : lint flake8 mypy

format : 
	$(AUTOFLAKE) --in-place --remove-unused-variables --recursive ./app ./tests
	$(BLACK) --preview ./app ./tests
.PHONY : format

dev-setup : 
	echo $(PWD) > ".venv/lib/python3.9/site-packages/ssaf.pth"
	$(MAKE) install
	$(PIP) install \
		--index-url "$(PIP_INDEX_URL)" \
		--requirement requirements.test.txt \
		--constraint constraints.txt
	$(PYTHON) -m pre-commit install
.PHONY : dev-setup

build :
	$(PYTHON) setup.py sdist bdist_wheel
.PHONY : build

upload-build :
	twine upload --repository-url https://gitlab.com/api/v4/projects/44976563/packages/pypi dist/* -u $(PIP_USER_NAME) -p $(PIP_PASSWORD)
.PHONY : upload-build

unit-test : 
	pytest --cov=auth test/unit
.PHONY : unit-test

integration-test : 
	pytest --cov=auth test/integration
.PHONY : integration-test

all-test : 
	pytest --cov=auth test
.PHONY : all-test

app-perm : 
	@dir_path="${PWD}/auth/routers"; \
    pattern='permissions=\["([^"]*)"\]'; \
    matches=(); \
    for file in "$$dir_path"/*; do \
        if [[ -f "$$file" ]]; then \
            file_matches=($$(awk -F'[="]' 'match($$0, /'"$$pattern"'/) {print substr($$0, RSTART+13, RLENGTH-14)}' "$$file")); \
            matches+=($${file_matches[@]}); \
        fi; \
    done; \
    output=$$(IFS=,; echo "$${matches[*]}"); \
    echo "[$$output]"
.PHONY : app-perm
