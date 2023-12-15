# Prerequisites

- Login to Eventbrite and generate a token here is the guide https://www.eventbrite.com/platform/docs/authentication#get-a-private-token
make sure to use ngrok in order to run it locally while creating the API_KEY for the local environment.

- Install docker on your machine
https://docs.docker.com/engine/install/

- Copy the private token to settings.py `EVENTBRITE_0AUTH_TOKEN`  variable
- After that generate the organization id by running the following command
`docker-compose run --rm web python manage.py get_org_id` and copy the output to settings.py variable `ORGANIZATION_ID`

# Installation

1) Run `docker-compose build`
2) Run `docker-compose up`


## Pre-commit
1) create a python3 virtual-env and activate it.
2) run `pip install pre-commit==2.20.0`
3) Run pip install pre-commit and install in via `pre-commit install`
4) Now it will execute when you commit the code and run in manually by `pre-commit run`
