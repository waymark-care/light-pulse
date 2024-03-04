# Light Pulse

## Description

Fiddling around and playing with Python APIs, a test project with the 10% time

## Table of Contents

- [Light Pulse](#light-pulse)
  - [Description](#description)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Testing](#testing)

## Installation

Based on the [FastAPI](https://fastapi.tiangolo.com/) documentation

This project is using `pipenv` as a dependency manager.
Install this package manager with `pip install --user pipenv`
- Install project requirements with `pipenv install`
- Activate an active terminal with `pipenv shell`

## Usage

Once everything is installed, run with: 
```
uvicorn main:app --reload --log-config=log_conf.yaml
```

You can go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for the documentation
on how to use the endpoints, and then [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
for alternative API documentation which generates documentation from OpenAPI definitions. 

## Testing
From the root directory, run `pytest` to run all the tests.
