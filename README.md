
Прототип инструмента для статической валидации SQL-запроса.

Позволяет проводить семантическую и синтаксические проверки raw-запросов в коде на python.

На данный момент реализована поддержка только для psycopg2.

Для запуска необходимо прописать параметры подключения к БД в файле pyproject.toml, база данных может не содержать записей.

Запуск тестов
```
python scripts/run_tests.py
```


Запуск mypy с плагином на произвольном файле (необходимо поднять БД и задать параметры подключения)
```
mypy [path to file] --config-file [path to config file with plugin]

mypy  tests/resources/database/correct_types_func.py --config-file setup.cfg
```
