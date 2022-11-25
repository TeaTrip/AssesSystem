# Система разметки данных для проекта по ИАД

Система предназначена для поиска и разметки изображений.

## Mongo DB

### Setup
Скачать и установить MongoDB 6.0.2 Community
Оставить стандартный порт при установке - 27017
Создать новую базу 'asses' и 3 таблицы в ней - 'sessions', 'users', 'images'

### Usage
Получить размеченные изображения можно отфлитровавав базу по параметру accepted

## Сбор изображений
### Install dependencies
```bash
pip install scrapy validators
```
### Usage
```
cd imgscrape
python collect.py
```

## Телеграм бот
### Install dependencies
```bash
pip install -r access_bot/requirements.txt
```

### Usage
```
cd access_bot
python main.py
```