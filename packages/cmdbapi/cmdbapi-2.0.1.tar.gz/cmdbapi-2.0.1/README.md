s# CMDBAPI

## Краткое описание
Python библиотека для взаимодействия с CMDB API

# Инициализация

```
cmdb=CMDBAPI(api_host='https://cmdapi.example.com:5000', api_user='secretuser',api_password='secretpassword',debug_mode=False,api_timeout=10)
```

* api_host - точка подключения к API (Обязательный параметр)

* api_user,api_password - имя пользователя и пароль для авторизации (Необязательный параметр.). Если их не указать работа возможна только с анонимными методами.

* debug_mode = Режим отладки (Если True), то будут делаться выводы отправки API запросов.

* api_timeout - таймаут ожидания ответа от API. Задается в секундах.

# Основные методы
Существует два свособа обращения к API. 

## Магические методы (Простые GET запросы)
Пример 1, GET API метод /v1/host можно вызвать так:
```
syscatalogs=cmdb.get.host()
```

Пример 2, GET API метод /v1/hostgroup можно вызвать так:
```
syscatalogs=cmdb.get.host()
```

## api_request

```
cmdb.api_request(api_type='post',api_method='agent/roles',**params)
```

* api_type - тип запроса (Прддерживаются: get,post,put,delete). По умолчанию - get

* api_method - метод вызова (Например для API /v1/agent/roles - метод agent/roles) 

* params - словарь аргументов запрашиваемого метода.

# Возможные ошибки

* api_host can not have value 'None' - при инициализации класса не передана точка подключения (api_host)

* Can not connect to API. ErrorCode: XXX. Response: ... - Ошибка подключения к API при авторизации и (или) вернулся код ответа отличный от 2XX.

* API request failed with error. ErrorCode: XXX. Response: ... - При запросе к API  вернулся код ответа отличный от 2XX

* Failed to parse JSON response - пришел от API ответ, который нельзя распарсить для обработки


# Пример использования
```
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

cmdb=CMDBAPI(config['cmdbapi']['host'],config['cmdbapi']['login'],config['cmdbapi']['pass'],config['cmdbapi']['timeout'])
syscatalogs=cmdb.get.host()
hstsnames_ = cmdb.get.hoststate()
isnames_ = cmdb.get.informsystem()
for syscatalog in syscatalogs:
    host_data=cmdb.api_request(api_method="host/"+str(syscatalog['code']))

....    
....

```
