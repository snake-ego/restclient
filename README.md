# REST API Client

Библиотека поставляет способ организации запросов к RESTFul API сервисам

## Changelog

### v2.4.4

* Исправлена ошибка в объявлении абстрактного свойства `BaseResponse.text`

### v2.4.3

* Исправлена генерация прараметров из списка в `url`

### v2.4.2

* Исправлен динамический поиск версии

### v2.4.1

* Upgaded `httpx`: `0.15` -> `0.17`
* `poetry` - основной инструмент для работы с пакетами

### v2.4.0

* Upgaded `httpx`: `0.11.1` -> `0.15.x`

### v2.3.0

* Added `BypassAuth` for proxying authorization header

### v2.2.0

* Added `auth` module for support httpx auth argument with classes:
  * `Auth` - base class
  * `BasicAuth` - simple `Basic` auth by username and password pair
  * `TokenAuth` - use `Bearer` auth by token

### v2.1.2

* Added support for `MappingProxyType` endpoints and headers initialization

### v2.1.1

* Added methods for changing endpoints and headers

### v2.1.0

* Used dataclasses for extra parameters

### v2.0.2

* Extend default timeouts to 30s

### v2.0.1

* Removed `requests` imports

### v2.0.0

### v1.2.1

### v1.2.0

### v1.1.1

### v1.1
