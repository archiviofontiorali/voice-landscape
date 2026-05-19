# Docker instruction (production)

```shell
# Create db, adminer, nginx and app containers and volumes
$ docker compose up --build

# Init database
$ docker compose exec app python manage.py migrate

# Other useful commands
$ docker compose exec app python manage.py migrate --noinput
$ docker compose exec app python manage.py createsuperuser
$ docker compose exec app python manage.py flush --no-input
```