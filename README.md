# Spicy CRM

## About

This is the Spicy Carrot tech challenge.

## Local setup

Create a virtual environment and install the dependencies:

```bash
python -m venv ~/.virtualenvs/spicy-crm
source ~/.virtualenvs/spicy-crm/bin/activate
pip install -r requirements.txt
```

Create a database and user for the project:

```bash
python manage.py migrate
python manage.py createsuperuser
```

Copy the existing .env.example file to .env and update the values as needed.

## Running tests

```bash
pytest
```

## Ingesting reading files

```bash
python manage.py ingest_readings_file <client-name> <file-path>
```

### Potatoes client

```bash
python manage.py ingest_readings_file potatoes tests/fixtures/potatoes/readings.json
```

### Carrot client
ingest carrot client data using below command
```bash
python manage.py ingest_readings_file carrots tests/fixtures/carrots/readings.txt
```


###### Decisions I made to make this better
Covert client folder into the django app and add a Client model with unique code and app_id
which will be shared in each request header and thus can easily distinguish the clients in 
request and provide the config details accordingly

Added a new base DateTimeStampModel for stamping datetime of creation & update of each entry in any model

Added a new endpoint <b>readings/v2/<supply_point_identifier></b> so that old API can still provide the support for pervious versions of the Apps

I've added one more model name as Manufacturer and mapped with meter table (for carrot) and added few flags
in meter and reading table and cross-checking that in the response

Changed the response for the API with two keys status - Boolean & data - Response

Not very sure about the time_code so kept it blank and not using it anywhere else

primarly focused on the carrots client

###### Scopes for further improvement
We can django rest framework for the APIs and accordingly its features. Also, use middleware in that to 
remove the dependency for expliclity checking the Client App ID

Should introduce caching so that same responses won't hit DB unnecessarily for API endpoints

We can make the admin views better for Ops team like inline support

Currently, there are not many validations put while ingesting the data which can also be done and should have a 
single view or endpoint to enter readings into the system.

Can create a standard responseformat and parse the response accordingly for every API for better understanding 

Should introduce the  logs for debugging purposes

Can write more testcases for the different clients

Also, after sometime depending on the usecase, we can create separate databases (connections handling through Routers) for each
client and can scale the things accordingly

we can also set up a documentation using swagger for better understanding of APIs and functions

Can set instructions for better understanding how one easily add the clients as per the requests

