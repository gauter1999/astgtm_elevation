import multiprocessing
from config import INPUT_DIR, CLICKHOUSE_CONFIG, TABLE_NAME
from utils.paths import find_dem_tif_files
from database.clickhouse import get_clickhouse_client, create_table, create_database
from processing.parallel_processor import process_and_upload_in_batches
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def main():
    client = get_clickhouse_client(CLICKHOUSE_CONFIG)
    create_database(client, CLICKHOUSE_CONFIG["database"])
    table_name = TABLE_NAME
    create_table(client, table_name)

    files = find_dem_tif_files(INPUT_DIR)
    # files = files[:10]
    logging.info(f"Найдено {len(files)} файлов")

    process_and_upload_in_batches(
        file_paths=files,
        client=client,
        table_name=table_name,
        max_workers=6,
        files_per_batch=120,
    )
    logging.info("Все файлы обработаны и загружены в ClickHouse")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()