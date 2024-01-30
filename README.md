# Light Pulse

## Description

A brief description of the project.

## Table of Contents

- [Light Pulse](#light-pulse)
  - [Description](#description)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Testing](#testing)

## Installation

Based on the [FastAPI](https://fastapi.tiangolo.com/) documentation:
- create a Python virtual environment, named `.venv`. Recommended instructions are on the Visual
Studio code website, so that you setup the Python development environment correctly. 
- Activate it with `source .venv/bin/activate`
- Install all the requirements with `pip install -r requirements.txt`

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
