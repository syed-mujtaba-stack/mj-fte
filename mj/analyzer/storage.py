import os
import shutil
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

from mj.config.settings import settings


@dataclass
class FolderSize:
    path: Path
    size: int
    file_count: int
    subfolders: List["FolderSize"] = field(default_factory=list)

    def __lt__(self, other):
        return self.size > other.size


@dataclass
class StorageInfo:
    total_space: int
    used_space: int
    free_space: int
    drive: str
    top_folders: List[FolderSize] = field(default_factory=list)
    junk_size: int = 0
    dangerous_size: int = 0
    protected_size: int = 0

    @property
    def free_percentage(self) -> float:
        if self.total_space == 0:
            return 0.0
        return (self.free_space / self.total_space) * 100

    @property
    def used_percentage(self) -> float:
        return 100 - self.free_percentage


class StorageAnalyzer:
    def __init__(self, drive: str = "C:\\"):
        self.drive = drive
        self._folder_cache: Dict[Path, FolderSize] = {}

    def get_drive_space(self) -> tuple[int, int, int]:
        total, used, free = shutil.disk_usage(self.drive)
        return total, used, free

    def analyze(self, scan_results=None, scan_root: str = None) -> StorageInfo:
        total, used, free = self.get_drive_space()

        info = StorageInfo(
            total_space=total,
            used_space=used,
            free_space=free,
            drive=self.drive,
        )

        if scan_results:
            info.junk_size = sum(f.size for f in scan_results.junk_files)
            info.dangerous_size = sum(f.size for f in scan_results.dangerous_files)
            info.protected_size = sum(f.size for f in scan_results.protected_files)

            root = Path(scan_root) if scan_root else self.drive
            folder_sizes = self._calculate_folder_sizes(scan_results.files, root)
            info.top_folders = self._get_top_folders(folder_sizes, root, 20)

        return info

    def _calculate_folder_sizes(self, files, stop_at: Path) -> Dict[Path, FolderSize]:
        folder_data: Dict[Path, dict] = defaultdict(lambda: {"size": 0, "count": 0})
        stop = Path(stop_at)

        for file_info in files:
            size = file_info.size
            current = file_info.path.parent
            while True:
                folder_data[current]["size"] += size
                folder_data[current]["count"] += 1
                if current == stop or current.parent == current:
                    break
                current = current.parent

        result = {}
        for path, data in folder_data.items():
            result[path] = FolderSize(
                path=path,
                size=data["size"],
                file_count=data["count"],
            )

        return result

    def _get_top_folders(self, folder_sizes: Dict[Path, FolderSize], root: Path, limit: int) -> List[FolderSize]:
        children = [
            fs for path, fs in folder_sizes.items()
            if path.parent == root
        ]
        children.sort()
        return children[:limit]

    def get_folder_tree(self, path: Path, max_depth: int = 3, current_depth: int = 0) -> FolderSize:
        if current_depth >= max_depth:
            return FolderSize(path=path, size=0, file_count=0)

        try:
            total_size = 0
            total_count = 0
            subfolders = []

            for entry in path.iterdir():
                if entry.is_file():
                    try:
                        total_size += entry.stat().st_size
                        total_count += 1
                    except (PermissionError, OSError):
                        pass
                elif entry.is_dir():
                    sub = self.get_folder_tree(entry, max_depth, current_depth + 1)
                    total_size += sub.size
                    total_count += sub.file_count
                    subfolders.append(sub)

            subfolders.sort()
            return FolderSize(path=path, size=total_size, file_count=total_count, subfolders=subfolders)
        except (PermissionError, OSError):
            return FolderSize(path=path, size=0, file_count=0)