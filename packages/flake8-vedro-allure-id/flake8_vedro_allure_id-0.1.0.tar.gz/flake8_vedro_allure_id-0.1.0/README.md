# flake8-vedro-allure-id

[![Tests](https://github.com/your-org/flake8-vedro-allure-id/actions/workflows/tests.yml/badge.svg)](https://github.com/your-org/flake8-vedro-allure-id/actions/workflows/tests.yml)
[![PyPI version](https://badge.fury.io/py/flake8-vedro-allure-id.svg)](https://badge.fury.io/py/flake8-vedro-allure-id)
[![Python versions](https://img.shields.io/pypi/pyversions/flake8-vedro-allure-id.svg)](https://pypi.org/project/flake8-vedro-allure-id/)

Flake8 плагин для проверки наличия декоратора `@allure.id()` для классов Scenario в тестах на базе Vedro.

## Установка

```bash
pip install flake8-vedro-allure-id
```

Или из исходников:

```bash
pip install -e .
```

## Использование

После установки плагин автоматически интегрируется с flake8. Для запуска проверки выполните:

```bash
flake8 path/to/your/tests
```

Для проверки только ошибок, генерируемых этим плагином:

```bash
flake8 path/to/your/tests --select=UGC
```

## Проверки

Плагин выполняет следующие проверки:

- **UGC100**: Класс Scenario должен иметь декоратор `@allure.id()`. Этот код ошибки возникает, когда импорт `allure` присутствует, но декоратор `@allure.id()` отсутствует.
- **UGC101**: Импортируйте `allure` и добавьте декоратор `@allure.id()` для класса Scenario. Этот код ошибки возникает, когда нет ни импорта `allure`, ни декоратора.

## Примеры

### Правильный код

```python
import allure
import vedro

@allure.id(12345)
class TestSomething(vedro.Scenario):
    pass
```

### Неправильный код

```python
import allure
import vedro

# Не указан декоратор @allure.id()
class TestSomething(vedro.Scenario):
    pass
```

```python
import vedro

# Нет ни импорта allure, ни декоратора @allure.id()
class TestSomething(vedro.Scenario):
    pass
```

## Разработка

### Установка для разработки

```bash
git clone https://github.com/your-org/flake8-vedro-allure-id.git
cd flake8-vedro-allure-id
pip install -e .
```

### Запуск тестов

```bash
pytest
```

## Публикация новой версии

1. Обновите версию в файле `flake8_vedro_allure_id_plugin/__init__.py`
2. Создайте новый тег в формате `vX.Y.Z`
3. Опубликуйте тег на GitHub
4. GitHub Actions автоматически опубликует пакет в PyPI, используя Trusted Publishing

### Настройка Trusted Publishing для PyPI

Для публикации пакета в PyPI через GitHub Actions мы используем метод Trusted Publishing:

1. Перейдите в настройки вашего проекта на PyPI: https://pypi.org/manage/account/publishing/
2. Создайте новую конфигурацию Trusted Publishing с использованием GitHub Actions
3. Укажите имя репозитория, рабочий процесс (workflow) и триггер (ref pattern: `refs/tags/v*`)
4. Workflow уже настроен с разрешением `id-token: write` для работы Trusted Publishing

## Лицензия

MIT 