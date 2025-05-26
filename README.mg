# ElevationH3 — Процессор высот из GeoTIFF в ClickHouse

Этот проект предназначен для обработки GeoTIFF-файлов с данными о высотах и загрузки точек в ClickHouse.

![Визуализация данных. Москва 8 уровень h3](images/elevation_8_level.png)


## Возможности
- Параллельная обработка TIFF-файлов
- Формирование широты/долготы
- Загрузка в ClickHouse
- Поддержка конфигураций

## Установка

```bash
poetry install

1. Находим и скачиваем данные в https://search.earthdata.nasa.gov/search/granules?p=C1711961296-LPCLOUD&pg[0][v]=f&pg[0][gsk]=-start_date&q=astgtm&tl=1168862400!5!!
2. Создаем базу в  clickhouse 'CREATE DATABASE IF NOT EXISTS geodata'
3. В config.py в переменную INPUT_DIR пишем путь с tif файлами.
4. Запускаем main.py