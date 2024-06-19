## Local setup

Create a virtual environment and install the dependencies:

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
ingest carrot client data using the below command
```bash
python manage.py ingest_readings_file carrots tests/fixtures/carrots/readings.txt
```

