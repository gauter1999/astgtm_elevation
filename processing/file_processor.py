import numpy as np
from rasterio.transform import Affine
from rasterio import open as raster_open
from skimage.transform import resize
from typing import Tuple, List
from pathlib import Path
from config import TARGET_SIZE


def process_tif_file(filepath: str | Path, target_size: Tuple[int, int] = None) -> List[Tuple[float, float, int]]:
    """
    Обрабатывает один .tif файл:
        - читает высоты
        - уменьшает матрицу
        - строит координатные сетки
        - фильтрует точки без данных

    :param filepath: Путь к файлу
    :param target_size: Размер выходного изображения
    :return: Список кортежей (lat, lon, elevation)
    """
    target_size = target_size or TARGET_SIZE
    elevation, transform = read_dem_tif_file(filepath)
    elevation_small = downsample_matrix(elevation, target_size=target_size)
    lats_full, lons_full = create_lat_lon_grids(*elevation.shape, transform)
    lats_small = resize(lats_full, target_size, order=1, preserve_range=True)
    lons_small = resize(lons_full, target_size, order=1, preserve_range=True)

    lat_flat = lats_small.flatten()
    lon_flat = lons_small.flatten()
    elev_flat = elevation_small.astype(int).flatten()

    lat_final, lon_final, elev_final = filter_valid_points(lat_flat, lon_flat, elev_flat)

    return list(zip(lat_final.tolist(), lon_final.tolist(), elev_final.tolist()))


def read_dem_tif_file(path: str | Path) -> Tuple[np.ndarray, Affine]:
    """Читает GeoTIFF и возвращает массив высот и трансформацию"""

    with raster_open(str(path)) as src:
        elevation = src.read(1).astype(np.float32)
        transform = src.transform
        if src.nodata is not None:
            elevation[elevation == src.nodata] = np.nan
        return elevation, transform


def downsample_matrix(data: np.ndarray, target_size: Tuple[int, int]) -> np.ndarray:
    """Уменьшает размер матрицы с сохранением диапазона значений"""
    return np.round(
        resize(data, target_size, preserve_range=True, anti_aliasing=True, mode="reflect")
    ).astype(np.int16)


def create_lat_lon_grids(height: int, width: int, transform: Affine) -> Tuple[np.ndarray, np.ndarray]:
    """Создаёт сетки широты и долготы"""
    cols, rows = np.meshgrid(np.arange(width), np.arange(height))
    xs, ys = transform * (cols.flatten(), rows.flatten())
    lats = np.reshape(ys, (height, width))
    lons = np.reshape(xs, (height, width))
    return lats, lons


def filter_valid_points(*arrays: np.ndarray) -> list[np.ndarray]:
    """Фильтрует точки с NaN"""
    valid_mask = ~np.isnan(arrays[0])
    for arr in arrays[1:]:
        valid_mask &= ~np.isnan(arr)

    return [arr[valid_mask] for arr in arrays]
