# Простой парсер данных с DDNet Master Servers и DDStats

Данный парсер упрощает получение данных с [мастера серверов дднета](https://master1.ddnet.org/ddnet/15/servers.json), а также предоставляет парсер [статистики игрока](https://ddstats.tw/)

## Установка библиотек:
```
pip install requests
```
## Установка парсера:
```
git clone https://github.com/neyxezz/ddnet-parser.git ddnet_parser
```
Важно понимать, что у меня пока что нет возможности выложить данный модуль на pypi (у меня не получилось), поэтому помещайте вручную эту папку в директорию выполнения вашего скрипта, либо можно сделать так:

```python
import sys
sys.path.append("ВАША_ДИРЕКТОРИЯ_ГДЕ_НАХОДИТСЯ_ПАПКА")
```
Теперь, вы сможете в полной мере пользоваться данной библиотекой.

## GetClients(address=None)
*  Получает объект для парсинга информации о клиентах
*  Документация: [🙂](https://github.com/neyxezz/ddnet-parser/blob/main/docs/docs.md#%D0%BA%D0%BB%D0%B0%D1%81%D1%81-clientsparser)
*  Args: address(bool, optional): адрес сервера, для которого нужно получить информацию о клиентах

Пример:
```python
from ddnet_parser import GetClients

clients = GetClients()
print(clients.get_clients(count=True))
```
## GetServers(address=None)
*  Получает объект для парсинга информации о серверах
*  Документация: [🙂](https://github.com/neyxezz/ddnet-parser/blob/main/docs/docs.md#%D0%BA%D0%BB%D0%B0%D1%81%D1%81-serversparser)
*  Args: address(bool, optional): адрес сервера, для которого нужно получить информацию

Пример:
```python
from ddnet_parser import GetServers

servers = GetServers()
print(servers.get_count())
```
## GetPlayerStats(name)
*  Получает объект для парсинга статистики игрока
*  Документация: [🙂](https://github.com/neyxezz/ddnet-parser/blob/main/docs/docs.md#%D0%BA%D0%BB%D0%B0%D1%81%D1%81-playerstatsparser)
*  Args: name(str): ник, для которого нужно получить статистику

Пример:
```python
from ddnet_parser import GetPlayerStats

player = GetPlayerStats("neyxezz")
print(player.get_total_seconds_played())
```
## GetMap(_map)
* Получает объект для парсинга данных карты
*  Документация: [🙂](https://github.com/neyxezz/ddnet-parser/blob/main/docs/docs.md#%D0%BA%D0%BB%D0%B0%D1%81%D1%81-mapsparser)
*  Args: address(str): карта, для которой нужно получить данные

Пример:
```python
from ddnet_parser import GetMap

map = GetMap("Linear")
print(map.get_mapper())
```
## GetProfile(name)
*  Получает объект для парсинга профиля игрока
*  Документация: [🙂](https://github.com/neyxezz/ddnet-parser/blob/main/docs/docs.md#%D0%BA%D0%BB%D0%B0%D1%81%D1%81-profileparser)
*  Args: name(str): ник, для которого нужно получить профиль

Пример:
```python
from ddnet_parser import GetProfile

profile = GetProfile()
print(profile.get_points())
```
## Подробная документация с примерами:
*  Подробная документация: [🙂](docs/docs.md)
*  Примеры: [🙂](examples/examples.py)

## Связь со мной
tg main: @neyxezz, tg twink: @neyxezz_twink
