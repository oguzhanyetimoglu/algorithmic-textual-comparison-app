# Backend

Always run in a virtual environment:

```shell
poetry shell
```

Check if everything is correct:

```shell
./manage.py check
```

Load initial data from fixtures:

```shell
./manage.py loaddata # TODO
```

Run a development server:

```shell
./manage.py runserver 8001
```

Database interactions:

```shell
./manage.py showmigrations
./manage.py makemigrations
./manage.py migrate
```
