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


