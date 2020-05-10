# openFDA-exploration
Python package and analyses of openFDA API queries

## Repo structure

```
| notebooks
     disease_reactions.ipynb                 # Association of different adverse effects with different disease areas
     drugs_taken_together.ipynb              # Drugs taken together
     disease_reactions_countries.ipynb       # Exploring different adverse events reported in different countries
| data                                       # Contains API key file
| src                                        # Code directory
     api.py                                  # Module containing helper methods and extraction scripts
     parser.py                               # Module containing helper methods and extraction scripts
     utils.py                                # Module containing helper methods and extraction scripts
| test                                       # Tests directory
```

## Installation
Install pipenv first `pip install pipenv`.  To make updated installation use 
`pipenv install -e .`. To install using the last successful packages version fix use
`python -m pipenv sync`.


## Usage
```
usage: runner.py [-h] [--num_time_ranges NUM_TIME_RANGES]
                 [--parse_from_crawled] [--db_dir DB_DIR]

optional arguments:
  -h, --help            show this help message and exit
  --num_time_ranges NUM_TIME_RANGES
  --parse_from_crawled  parse previously saved records
  --db_dir DB_DIR       parse previously saved records```

To run crawler for downloading records from openFDA run:
```
pipenv run python ./runner.py --num_time_ranges=2
```
Results will be saved into json database under directory `db_dir_%Y-%m-%d-%H`

To parse previously downloading from openFDA records run:
```
pipenv run python ./runner.py --db_dir db_dir_2020-05-10-10 --parse_from_crawled
```
db_parsed_drugindication.json, db_parsed_reaction_by_country.json and db_parsed_taken_together.json