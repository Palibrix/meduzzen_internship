# Meduzzen Internship FastAPI application
## To run project, run this in terminal:
``
pip install -r requirements.txt
``
``
uvicorn app.main:app
``
## To run tests, run this in terminal:
``
pytest
``
## To start app with Docker, run this in terminal:
``
docker-compose up --build -d
``

## Creating migrations
To create migrations, you need to open container terminal
``
docker-compose exec web sh
``
and run 
``
alembic revision --autogenerate -m "Comment"
``

## Applying migrations
To apply migrations, you need to open same container terminal and run 
``
alembic upgrade head
``
Use ``sudo chown -R $(whoami) .`` if you have problems with docker-created files ownership

***Note:***
*To run tests, you need to start Docker Compose with **docker-compose-test.yml** file:*
``
docker-compose -f docker-compose-test.yml up --build
``
