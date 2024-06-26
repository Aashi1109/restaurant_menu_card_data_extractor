# Image data scrapper

## Description

- A scrapper projects which scraps images using either plain google search or using google programmable search API.
- Uses tesseract for OCR and saves extracted data as plain text in local sqlite database.

## Live Preview

### Homepage

![Homepage](https://res.cloudinary.com/aashish1109/image/upload/v1717866807/Internship/Restaurant%20Image%20Scrapper/ntojqmfhntmk6vfvpaco.png)

### Scrap task details page

![Task details page](https://res.cloudinary.com/aashish1109/image/upload/v1717867062/Internship/Restaurant%20Image%20Scrapper/xs93iiqwfgcilpkofcpk.png)

## Deployment usage

- Pass required env variables in the docker-compose.yml file
- ENV variables required for client
    - SCRAPER_API_URL
    - USE_CSE_PAPI
    - HOSTNAME
    - TASK_FETCH_INTERVAL
    - PORT
- ENV variables required for server
    - GOOGLE_CSE_ID
    - GOOGLE_API_KEY
    - CELERY_BACKEND
    - CELERY_BROKER
    - PORT
    - HOST
    - LOG_LEVEL
    - TEMP_FOLDER_PATH
- After passing the environment variables execute this command

```shell
docker compose up
```

- `Ensure that docker is installed on your system and redis is running`
- `Celery uses redis as backend and broker`
- `SQLite is local so it gets reset after restart of service.`

## Development usage

### Server configuration

From root folder of project run this command to start celery workers

```shell
celery -A server.src.worker.celery_app worker -f <log paths for celery logs> -E --pool=solo
```

Before running make sure env is activated

```shell
source ./<env path>/bin/activate
```

To start the fastapi application use the following command or you can use any IDE of your choice to run the application.

```shell
python -m server.src.main
```

### Client

Navigate to client directory and execute below commands

```shell
cd client
```

```shell
npm i
```

```shell
npm run dev
```