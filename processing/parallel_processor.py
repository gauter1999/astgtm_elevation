from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import List, Tuple, Union
from clickhouse_connect.driver.client import Client
from .file_processor import process_tif_file
from database.clickhouse import insert_data
import logging

PointRecord = Tuple[float, float, int]


def process_batch(file_batch: List[Union[str, Path]]) -> List[PointRecord]:
    """
    Обрабатывает группу файлов в одном процессе.
    """
    batch_results = []
    for filepath in file_batch:
        try:
            points = process_tif_file(filepath)
            batch_results.extend(points)
        except Exception as e:
            logging.error(f"[ERROR] {filepath}: {e}")
    return batch_results


def process_and_upload_in_batches(
    file_paths: List[Path],
    table_name: str,
    client: Client = None,
    max_workers: int = 6,
    files_per_batch: int = 100,
):
    """
    Обрабатывает файлы батчами и отправляет в ClickHouse
    """
    total_files = len(file_paths)
    for i in range(0, total_files, files_per_batch):
        logging.info(f"\n--- Батч {i // files_per_batch + 1} ---")
        batch_files = file_paths[i:i + files_per_batch]
        logging.info(f"Обрабатываю {len(batch_files)} файлов")

        all_points = process_multiple_files_in_parallel(batch_files, max_workers)

        if all_points:
            logging.info(f"Загружаю {len(all_points)} точек в ClickHouse...")
            insert_data(client, table_name, all_points)
        else:
            logging.info("Нет данных для загрузки в этом батче")


def process_multiple_files_in_parallel(
    file_paths: List[Union[str, Path]],
    max_workers: int = 6
) -> List[PointRecord]:
    """
    Обработка файлов в параллельном режиме (в одном батче)
    """
    results = []

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_batch, [file]) for file in file_paths]

        for future in as_completed(futures):
            try:
                batch_result = future.result()
                results.extend(batch_result)
            except Exception as e:
                logging.info(f"[FATAL] Ошибка при обработке файла: {e}")

    return results