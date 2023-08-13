# Docker instruction (production)

```shell
# Create db, adminer, nginx and app containers and volumes
$ docker compose up --build

# Init database
$ docker compose exec app python manage.py migrate
```