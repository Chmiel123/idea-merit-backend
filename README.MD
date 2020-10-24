# Idea Merit

This is the python flask backend part of the Idea Merit project.

### Install

```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```
### Configuration

Update `config/*_config.yml` with relevant data.

### Deploy database

Base configuration:
```
python run_sql.py
```

Test configuration:
```
python run_sql.py test
```

### Run unit tests

```
python run_tests.py
```

To run unit tests of the pattern `*pattern*_test.py`
```
python run_tests.py pattern
```

To run with coverage saved to tmp/coverage/index.html
```
python run_coverage.py
```

## Run production environment

TODO

## Links

[Technical documentation](doc/technical.md)