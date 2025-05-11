# core-aws-cdk
___________________________________________________________________________________________________________________

This project contains commons elements and constructs to create infrastructure
in AWS using AWS CDK...

## Execution Environment

### Install libraries
```shell
pip install --upgrade pip 
pip install virtualenv
```

### Create the Python Virtual Environment.
```shell
virtualenv --python=python3.11 .venv
```

### Activate the Virtual Environment.
```shell
source .venv/bin/activate
```

### Install required libraries.
```shell
pip install .
```

### Check tests and coverage...
```shell
python manager.py run-test
python manager.py run-coverage
```
