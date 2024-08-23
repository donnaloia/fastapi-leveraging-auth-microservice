# REST API written in fastapi that uses our external authentication and authorization services written in Gleam

## What is this for?
- A FastAPI project with a generic resource hierarchy, pagination, docs and detailed error handling.  The objective of this excercise was to build a middleware that hooks into our custom authz/authn services running on the Erlang VM.

## How to run?
- In the root dir:
    - Ensure Docker Desktop is running on your laptop
    - Run in the CLI:
        - docker-compose up --build

## How to test
- Use the examples provided in scratchpad.ipynb