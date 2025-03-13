# Запуск происходит посредством Docker

Создание миграций
```
docker-compose up --build -d
```
``` 
docker exec -it <container_id> /bin/bash    
```
``` 
python manage.py migrate    
python manage.py makemigrations    
```

# API для управления комнатами и бронированиями

## Комнаты

### 1. Создание комнаты

* **Описание**: Создает новую комнату с указанным описанием и ценой.
* **URL**: `POST /rooms/create`
* **Параметры запроса**:

| Параметр | Тип | Обязательный | Описание |
|----------|-----|-------------|----------|
| description | string | Да | Описание комнаты |
| price | decimal(10,2) | Да | Цена комнаты |

* **Пример запроса**:
```
curl -X POST -d "description=Уютная комната с видом на море" -d "price=7999.00" http://localhost:8000/api/rooms/create
```

* **Пример успешного ответа** (201 Created):
```json
{
  "success": "room was created: 1"
}
```

* **Пример ошибки** (400 Bad Request):
```json
{
  "price": ["Ensure that there are no more than 10 digits in total."]
}
```

### 2. Список комнат

* **Описание**: Получает список комнат, отсортированных по указанным параметрам.
* **URL**: `GET /rooms/list`
* **Параметры запроса**:

| Параметр | Тип | Обязательный | Описание |
|----------|-----|-------------|----------|
| sort_by | string | Нет | Поле для сортировки. Доступные значения: price, created_at. По умолчанию: created_at |
| order | string | Нет | Порядок сортировки. Доступные значения: asc, desc. По умолчанию: asc |

* **Пример запроса**:
```
curl -X GET "http://localhost:8000/api/rooms/list?sort_by=price&order=desc"
```

* **Пример успешного ответа** (200 OK):
```json
[
  {
    "id": 1,
    "description": "Уютная комната с видом на море",
    "price": "7999.00",
    "created_at": "2025-03-14T10:30:00Z"
  },
  {
    "id": 2,
    "description": "Стандартная комната с двумя кроватями",
    "price": "5999.00",
    "created_at": "2025-03-13T09:15:00Z"
  }
]
```

### 3. Удаление комнаты

* **Описание**: Удаляет комнату по указанному ID. Также удаляются все связанные с комнатой бронирования.
* **URL**: `DELETE /rooms/delete/{room_id}`
* **Параметры пути**:

| Параметр | Тип | Обязательный | Описание |
|----------|-----|-------------|----------|
| room_id | integer | Да | ID комнаты, которую нужно удалить |

* **Пример запроса**:
```
curl -X DELETE http://localhost:8000/api/rooms/delete/1
```

* **Пример успешного ответа** (200 OK):
```json
{
  "success": "room was deleted"
}
```

## Бронирования

### 4. Создание бронирования

* **Описание**: Создает новое бронирование для указанной комнаты на заданные даты.
* **URL**: `POST /bookings/create`
* **Параметры запроса**:

| Параметр | Тип | Обязательный | Описание |
|----------|-----|-------------|----------|
| room | integer | Да | ID комнаты, которую нужно забронировать |
| date_start | date | Да | Дата начала бронирования (формат: YYYY-MM-DD) |
| date_end | date | Да | Дата окончания бронирования (формат: YYYY-MM-DD) |

* **Пример запроса**:
```
curl -X POST -d "room=1" -d "date_start=2025-03-01" -d "date_end=2025-05-05" http://localhost:8000/api/bookings/create
```

* **Пример успешного ответа** (201 Created):
```json
{
  "booking_id": 1
}
```

* **Пример ошибок** (400 Bad Request):
```json
{
  "non_field_errors": ["Start date must be before end date."]
}
```
```json
{
  "non_field_errors": ["Start date cannot be in the past."]
}
```
```json
{
  "non_field_errors": ["Room 1 is already booked for the selected dates."]
}
```

### 5. Список бронирований

* **Описание**: Получает список бронирований для указанной комнаты.
* **URL**: `GET /bookings/list`
* **Параметры запроса**:

| Параметр | Тип | Обязательный | Описание |
|----------|-----|-------------|----------|
| room_id | integer | Да | ID комнаты, для которой нужно получить список бронирований |

* **Пример запроса**:
```
curl -X GET "http://localhost:8000/api/bookings/list?room_id=1"
```

* **Пример успешного ответа** (200 OK):
```json
[
  {
    "id": 1,
    "room": 1,
    "date_start": "2025-05-01",
    "date_end": "2025-06-05"
  }
]
```

* **Пример ошибок** (400 Bad Request):
```json
{
  "error": "room_id is required"
}
```
```json
{
  "error": "room with id 999 does not exist"
}
```

### 6. Удаление бронирования

* **Описание**: Удаляет бронирование по указанному ID.
* **URL**: `DELETE /bookings/delete/{booking_id}`
* **Параметры пути**:

| Параметр | Тип | Обязательный | Описание |
|----------|-----|-------------|----------|
| booking_id | integer | Да | ID бронирования, которое нужно удалить |

* **Пример запроса**:
```
curl -X DELETE http://localhost:8000/api/bookings/delete/1
```

* **Пример успешного ответа** (200 OK):
```json
{
  "success": "room was deleted"
}
```