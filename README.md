- Start the stack with Docker Compose:
```
$ docker compose up -d --build
```

- Run migrations
```
$ alembic upgrade head
```