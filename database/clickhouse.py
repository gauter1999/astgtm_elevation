from typing import List, Tuple
import clickhouse_connect
import logging

def get_clickhouse_client(config):
    return clickhouse_connect.get_client(**config)


def create_database(client, db_name: str):
    client.command(f"CREATE DATABASE IF NOT EXISTS {db_name}")

def create_table(client, table_name: str):
    client.command(f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        lat Float64,
        lon Float64,
        elevation Int16
    ) ENGINE = MergeTree
    ORDER BY tuple()
    """)


def insert_data(
    client,
    table_name: str,
    data: List[Tuple[float, float, int]]
):
    column_names = ['lat', 'lon', 'elevation']
    client.insert(table_name, data, column_names)
    logging.info(f"Загружено {len(data)} точек в таблицу {table_name}")