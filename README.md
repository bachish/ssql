
Сборка окружения
```
poetry build
poetry config --list
```

Запуск тестов
```
python scripts/run_tests.py
```

-------------

> !Не тестировалось после изменений, временно не поддерживается!
Запуск mypy с плагином на произвольном файле (необходимо поднять БД и задать параметры подключения)
`
mypy tests/use_ssql.py --config-file setup.cfg
`
