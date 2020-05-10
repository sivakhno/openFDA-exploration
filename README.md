# openFDA-exploration
Python package and analyses of openFDA API queries

## Overview 



## Installation


### Package

Install pipenv first `pip install pipenv`.  To make updated installation use 
`pipenv install -e .`. To install using last successful packages version fix use
`python -m pipenv sync`.


### Environment variables

```
transcrypt -c aes-256-cbc -p $TRANSCRYPT_PASSWORD -y
```
For more information see `https://github.com/elasticdog/transcrypt`.

## Usage






## Logger, Linting and Typechecking
### Linter and Typechecker
```
python -m pipenv run flake8 --config=test/flake_config.ini
```

```
python -m pipenv src
```

### Logging

## Testing


```
pipenv run python -m pytest ./test -m unit
```
