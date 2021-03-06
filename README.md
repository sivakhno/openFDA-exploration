# openFDA-exploration
Python package and analyses of openFDA using adverse events [API](https://open.fda.gov/apis/drug/event/) queries. It uses multi-process parallelism to simultaneously download openFDA records and store them into TinyDB document databases. Command line wrapper provides checkpoint interface to separately download and parse openFDA records, while notebooks provide analyses of pre-processed data. Since openFDA interface restricts the number of records that can be downloaded via different API limits, such multi-parallel architecture allows to acquire larger number of records in shorter time frame. For example, it made possible to download 791200 records for analyses presented here faster.

## Repo structure
```
| notebooks
     disease_reactions.ipynb                 # Association of different adverse effects with different disease areas
     drugs_taken_together.ipynb              # Drugs taken together
     disease_reactions_countries.ipynb       # Exploring different adverse events reported in different countries
     csv files                               # Files storing key analyses from notebooks 
| data                                       # Contains API key file
| src                                        # Code directory
     api.py                                  # Module containing functions for retrieving records from openDFA using openDFA API
     parser.py                               # Module containing functions for parsing retrieved and saved records from openDFA
     utils.py                                # Module containing helper methods and extraction scripts
| test                                       # Tests directory
```

## Installation
Install pipenv first `pip install pipenv`.  To make updated installation use 
`pipenv install -e .`. To install using the last successful packages version fix use
`python -m pipenv sync`.


## Command line usage
```
usage: runner.py [-h] [--num_time_ranges NUM_TIME_RANGES]
                 [--parse_from_crawled] [--db_dir DB_DIR]

optional arguments:
  -h, --help            show this help message and exit
  --num_time_ranges NUM_TIME_RANGES
                        number of time periods to search over
  --parse_from_crawled  parse previously saved records
  --db_dir DB_DIR       path to db folder```
```
To run crawler for downloading records from openFDA use:
```
pipenv run python ./runner.py --num_time_ranges=2
```
This will start parallel processes based on the number of cpus and api keys provided (whichever is smaller). Results will be saved into json TinyDB database under directory `db_dir_%Y-%m-%d-%H`.

To parse previously downloading from openFDA records run:
```
pipenv run python ./runner.py --db_dir db_dir_2020-05-10-10 --parse_from_crawled
```
that will save pre-processed records under `db_dir_2020-05-10-10`


## Notebook analyses
To reproduce notebook analyses download openFDA records saved into TinyDB files `db_parsed_drugindication.json, db_parsed_reaction_by_country.json and db_parsed_taken_together.json` [from Google Drive](https://drive.google.com/open?id=1BSp7Mkxi2g34XPiC4lLHxmMTSk2WHJDg) and place under `notebooks` folder.
The files were generated by running pipenv run python `./runner.py --db_dir db_dir_2020-05-10-10 --parse_from_crawled`.
