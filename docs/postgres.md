# PostgreSQL
## How to backup
```shell
# Ensure .backup folder exists
$ mkdir -p .backup

# Dump db with pg_dump (with or without compression)
$ pg_dump -U DB_USER DB_NAME > .backup/landscapes."$(date --iso-8601=seconds)".sql
$ pg_dump -U DB_USER DB_NAME | gzip -9 > .backup/landscapes."$(date --iso-8601=seconds)".sql.gz

# On docker 
$ docker exec -i CONTAINER_NAME pg_dump -U DB_USER DB_NAME > .backup/landscapes."$(date --iso-8601=seconds)".sql
$ docker exec -i CONTAINER_NAME pg_dump -U DB_USER DB_NAME | gzip -9 > .backup/landscapes."$(date --iso-8601=seconds)".sql.gz
```

## How to restore
```shell
# NOTE: remember to create database first
$ psql -U DB_USER DB_NAME < .backup/BACKUP_NAME.sql 

# docker variant
$ cat .backup/BACKUP_NAME.sql | docker exec -i CONTAINER_NAME psql -U DB_USER DB_NAME 
```

## Tips and tricks
Restore the latest backup starting with landscapes
```shell
gzip -dk $(ls .backup/landscapes.*.gz | tail -1)
psql voci < $(ls .backup/landscapes.* | tail -1)
```