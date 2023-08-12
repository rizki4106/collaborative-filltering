# Collaborative filltering

This program is implementation of collaborative fillter ( user to user )

## How to Run

create `.env` file in your root dir

```.env
# DATABASE CONFIGURATION
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
QUERY=

# APP CONF
APP_PORT=
APP_NAME=
ROW_VALUE=
COLUMN_VALUE=

# DOCKER CONF
DOCKER_NETWORK=
```

development
```bash
pip3 install requirements.txt && uvicorn main:app --reload
```

Production
```bash
docker-compose up --build -d
```