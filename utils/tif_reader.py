from typing import Tuple, Optional, List
from pathlib import Path
import numpy as np
from rasterio.transform import Affine
import rasterio


def find_dem_tif_files(folder_path: str | Path) -> List[Path]:
    """
    Находит все .tif файлы в указанной папке, соответствующие маске:
        ASTGTMV003_*_dem.tif

    :param folder_path: Путь к папке с файлами
    :return: Список объектов Path к найденным файлам
    """
    pattern = "ASTGTMV003_*_dem.tif"
    return list(Path(folder_path).rglob(pattern))

def read_dem_tif_file(path: str | Path) -> Tuple[np.ndarray, Affine]:
    """
    Читает GeoTIFF файл с высотами.

    :param path: Путь к .tif файлу
    :return: Кортеж (elevation_array, transform)
    """
    path = Path(path)  # Приводим к типу Path
    with rasterio.open(str(path)) as src:
        elevation = src.read(1).astype(np.float32)
        transform = src.transform
        if src.nodata is not None:
            elevation[elevation == src.nodata] = np.nan
        return elevation, transform