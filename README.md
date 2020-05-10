# openFDA-exploration
Python package and analyses of openFDA API queries
# Skills XGboost Model 

## Overview 

Skills prediction training and serving module based on AWS SageMaker framework. 
All operations are available through single Docker container for cohesivness and simplicity.
The training workflow creates model atchitecture, extracts relevant training data from databases (if needed) and performs training. 
After training models are stored to an s3 bucket, while perofmance metrics to `model-metrics` database.
Serving command creates the relevant endpoint with autoscaling.

### Modelling approach  
The design of skill model is based on the recommender engine principle: we assume that, when large numbers of individuals are considered, skills will tend to group by roles and professions.  For example, when considering data scientists, they will have very similar skill sets. These skill sets will become more different when comparing them with software engineers. The overlap between skill sets of Data Scientists and Marketing Professionals will be even less pronounced. These observations allows us to build an algorithm that looks at skills co-occurence to establish similarity. For example, Pandas and Python are very likely to co-occur together, Python and Java less likely and Python and AutoCAD unlikely to co-occur. 

The model is based on the XGBoost algorithm, with one submodel for each skill. The model attempts to predict a skill from all other skills in a profile across all profiles. This model set-up is easily parallelizable by skill and that is what is done - skills are evenly split across AWS instances to speed-up computation. 



## Installation

`aws configure` should be run and AWS access credential variables set.
You must have python version `3.7` installed. 

### Package

Install pipenv first `pip install pipenv`.  To make updated installation use 
`pipenv install -e .`. To install using last successful packages version fix use
`python -m pipenv sync`.

### Docker

Run `./build_and_push_docker.sh`, this will tag docker image and push to AWS ECR repository. 

### Environment variables

You will need .env file with the following variables (or these environment variables in your shell session):
```
DB_HOST_INDEED='Crawled Indeed CVs for batch training data retrieval'
DB_HOST_MODELS='Information about models with accuracy metrics from training rounds'
SAGEMAKER_ROLE='AWS SageMaker Role Arn',
```

They are accessed from `env-variables` and can be decrypted via `transcrypt` (keys in LastPass)
with the following command:
```
transcrypt -c aes-256-cbc -p $TRANSCRYPT_PASSWORD -y
```
For more information see `https://github.com/elasticdog/transcrypt`.

## Usage

### Configuration

Currently parameters specifying versioning of docker images, model name and s3 buckets are stored
in `src/config.py`.  Model version and enpoint identifier can be specified via command line, 

### Training

Launch with default parameters using `pipenv run python ./deploy_from_training.py` or run
`./deploy_from_training.py --help`, in particular an AWS instance type is specified via `--instance` command and the number of instances - via `--instance_counts`. By default the call will create an endpoint at the end of training, this can be disabled with `--stop_at_training` checkpoint.
Results are saved to `model-metrics` database, schema can be found under
`src/db.py`.


### Creating endpoints

Launch with default parameters using `pipenv run python ./deploy_from_binary.py` or run
`./deploy_from_binary.py --help`. The endpoint will be created using the following naming convention
[{config.model_name}-endpoint-v{model_version}-{vendpoint}],
for which the values are derived from `src/config.py` file or command line parameters (`--vendpoint`).


### Calling endpoints

Endpoint can be envoked using a range of different APIs as specified in
`https://docs.aws.amazon.com/sagemaker/latest/dg/API_runtime_InvokeEndpoint.html`, for example
see below Python SDK commands. Endpoint expects JSON file with the mandatory keys `profile_skills` and `role_skills`.

'''
data={'profile_skills':['communication'],'role_skills':['web development']}
import json 
import boto3 
client = boto3.client('runtime.sagemaker')
response = client.invoke_endpoint(EndpointName=skills-xgboost-endpoint-v1-5',
                                  Body=json.dumps(data))
response_body = response['Body'] 
out = response_body.read()
json.loads(out.decode('utf-8'))
'''

## Logger, Linting and Typechecking
### Linter and Typechecker
```
python -m pipenv run flake8 --config=test/flake_config.ini
```

```
python -m pipenv run mypy src xgboost.py --ignore-missing-imports deploy_from_training.py deploy_from_binary.py
```

### Logging

Logging is available through AWS CloudWatch by default for each training, serving and endpoint
invocation jobs.

## Testing
Current implementation uses integration testing to check that endpoints are created correctly
and predictions intervals are within corret bounds.

To run invoke all tests run (-v = verbose):

```
pipenv run python -m pytest ./test -v
```

Integration tests will create endpoint and test returned confidence intervals,
to run only integration test run:

```
pipenv run python -m pytest ./test -m integration
```
Unit tests will load and interrogate results of the most recent trained model on select inputs,
to run only integration test run:

```
pipenv run python -m pytest ./test -m unit
```

Endpoints can also be tested via AWS CLI with the following command which saves the results
to `out.json`:

```
aws sagemaker-runtime invoke-endpoint \
  --endpoint-name work-experience-model-2019-07-12-13-44-44-927 \
  --body "$(cat test/test.json)" \
  --content-type application/json out.json
```


## Deployment 

### Local installation 


### CircleCI

CircleCI configuration includes Development and Production workflows for training and production workflow for creating serving endpoints. 

### Terraform

## References 

`https://medium.com/weareservian/machine-learning-on-aws-sagemaker-53e1a5e218d9`

