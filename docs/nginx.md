
## Nginx instructions
```shell
$ sudo cp nginx.conf /etc/nginx/sites-available/voci.afor.dev
$ sudo ln -s /etc/nginx/sites-available/voci.afor.dev /etc/nginx/sites-enabled/voci.afor.dev
$ sudo nginx -t # To check if configuration is valid
$ sudo nginx -s reload
$ sudo mkdir -p /usr/share/nginx/voice-landscape /usr/share/nginx/voice-landscape/static 

# Set DEBUG=1 and STATIC_ROOT and MEDIA_ROOT in .env to the last two created folders
 
$ make production
$ make bootstrap-db
$ sudo .venv/bin/python manage.py collectstatic
$ sudo .venv/bin/python manage.py compress --force
```

## YUNoHost (redirect + nginx configuration)
Install `redirect` app in YUNoHost `administration > applications > install`
1. Select a reasonable name
2. select domain
3. select path ("/" or "/django")
4. select http://127.0.0.1:8001 as redirection path
5. Select "Proxy Invisible (NGINX Proxy Pass) Everyone..."


```shell
# Add changes based on nginx.conf if path is / else use nginx.yunohost.conf as reference 
$ sudo vim /etc/nginx/conf.d/<domain>/conf.d/redirect.conf
$ sudo nginx -t # To check if configuration is valid
$ sudo nginx -s reload
$ sudo chown -R admin:1007 /usr/share/nginx/voice-landscape
$ sudo mkdir -p /usr/share/nginx/voice-landscape /usr/share/nginx/voice-landscape/static
```

Set in `.env`
- `DEBUG=false`
- `STATIC_ROOT=/usr/share/nginx/voice-landscape/static` 
- `MEDIA_ROOT=/usr/share/nginx/voice-landscape/media`

Generate static file, db and load previous site contents
```shell
$ sudo .venv/bin/python manage.py collectstatic
#$ sudo .venv/bin/python manage.py compress --force
#$ sudo .venv/bin/python manage.py runscript load_data
```

Load gunicorn service file and start/enable it
Remember to change user and/or repository path if different from .service file
```shell
$ sudo cp gunicorn.service /etc/systemd/system/gunicorn.service
$ sudo systemctl enable gunicorn
$ sudo systemctl start gunicorn
```