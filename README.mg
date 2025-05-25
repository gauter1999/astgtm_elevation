# ElevationH3 — Процессор высот из GeoTIFF в ClickHouse

Этот проект предназначен для обработки GeoTIFF-файлов с данными о высотах и загрузки точек в ClickHouse.

## Возможности
- Параллельная обработка TIFF-файлов
- Формирование широты/долготы
- Загрузка в ClickHouse
- Поддержка конфигураций

## Установка

```bash
poetry install

находим данные в https://search.earthdata.nasa.gov/search/granules?p=C1711961296-LPCLOUD&pg[0][v]=f&pg[0][gsk]=-start_date&q=astgtm&tl=1168862400!5!!
скачиваем
создаем базу в кликхаусе CREATE DATABASE IF NOT EXISTS geodata
запускаем main.py