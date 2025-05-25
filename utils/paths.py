from pathlib import Path
from typing import List

def find_dem_tif_files(folder_path: str | Path) -> List[Path]:
    """
    Находит все ASTGTMV003_*_dem.tif файлы рекурсивно
    """
    return list(Path(folder_path).rglob("ASTGTMV003_*_dem.tif"))