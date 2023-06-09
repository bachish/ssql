
Сборка окружения
```
poetry build
poetry config --list
```

Запуск тестов
```
python scripts/run_tests.py
```


Запуск mypy с плагином на произвольном файле (необходимо поднять БД и задать параметры подключения)
```
mypy [path to file] --config-file [path to config file with plugin]

mypy  tests/resources/database/correct_types_func.py --config-file setup.cfg
```
-------------

Если вызов mypy с *корректными* параметрами выдает ошибку:

```
setup.cfg:2: error: Error importing plugin "ssql.ssql_plugin": No module named 'ssql.ssql_plugin'  [misc]
```

То одна из причин - ошибка при компиляции файла. К сожалению, `mypy` не выдает подробного лога.
Чтобы обнаружить эти ошибки можно запустить `python` файл, который импортирует плагин. В нашем случае таким отладочным файлом служит `ex.py`

```
 python run ex.py
 ```
