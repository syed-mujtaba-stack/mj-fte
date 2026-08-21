import os
import time
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from tqdm import tqdm

from mj.config.settings import settings
from mj.analyzer.windows_rules import WindowsRules


@dataclass
class FileInfo:
    path: Path
    size: int
    is_junk: bool = False
    is_dangerous: bool = False
    is_protected: bool = False
    classification_reason: str = ""
    extension: str = ""
    folder: str = ""

    def __hash__(self):
        return hash(self.path)

    def __eq__(self, other):
        if isinstance(other, FileInfo):
            return self.path == other.path
        return False


@dataclass
class ScanResult:
    files: List[FileInfo] = field(default_factory=list)
    total_files: int = 0
    total_size: int = 0
    junk_files: List[FileInfo] = field(default_factory=list)
    dangerous_files: List[FileInfo] = field(default_factory=list)
    protected_files: List[FileInfo] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    scan_duration: float = 0.0

    def __post_init__(self):
        self.rebuild()

    def rebuild(self):
        self.total_files = len(self.files)
        self.total_size = sum(f.size for f in self.files)
        self.junk_files = [f for f in self.files if f.is_junk]
        self.dangerous_files = [f for f in self.files if f.is_dangerous]
        self.protected_files = [f for f in self.files if f.is_protected]


class FileScanner:
    def __init__(
        self,
        root: str = None,
        max_depth: int = None,
        workers: int = None,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ):
        self.root = Path(root or settings.scan_root)
        self.max_depth = max_depth or settings.max_scan_depth
        self.workers = workers or settings.parallel_workers
        self.progress_callback = progress_callback
        self.windows_rules = WindowsRules()
        self._stop_event = threading.Event()
        self._lock = threading.Lock()
        self._scanned_count = 0
        self._total_estimate = 10000

    def stop(self):
        self._stop_event.set()

    def _should_scan_folder(self, folder: Path, depth: int) -> bool:
        if depth > self.max_depth:
            return False
        if self.windows_rules.is_protected_path(folder):
            return False
        return True

    def _collect_files(self, folder: Path, depth: int, results: List[FileInfo]):
        if self._stop_event.is_set():
            return

        try:
            entries = list(folder.iterdir())
        except (PermissionError, OSError):
            return

        for entry in entries:
            if self._stop_event.is_set():
                break

            try:
                if entry.is_file():
                    self._process_file(entry, results)
                elif entry.is_dir():
                    if self._should_scan_folder(entry, depth):
                        self._collect_files(entry, depth + 1, results)
            except (PermissionError, OSError):
                continue

    def _process_file(self, file_path: Path, results: List[FileInfo]):
        try:
            stat = file_path.stat()
            size = stat.st_size

            if size < settings.min_file_size_mb * 1024 * 1024:
                return

            ext = file_path.suffix.lower()
            folder = str(file_path.parent).lower()

            is_protected = self.windows_rules.is_windows_file(file_path)
            protected_reason = ""
            if is_protected:
                protected_reason = self.windows_rules.get_protected_reason(file_path) or "Protected by Windows rules"

            file_info = FileInfo(
                path=file_path,
                size=size,
                is_protected=is_protected,
                classification_reason=protected_reason,
                extension=ext,
                folder=folder,
            )

            with self._lock:
                results.append(file_info)
                self._scanned_count += 1
                if self.progress_callback:
                    self.progress_callback(self._scanned_count, self._total_estimate)

        except (PermissionError, OSError):
            pass

    def _run_scan(self, all_files: List[FileInfo]):
        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            futures = []
            try:
                root_entries = list(self.root.iterdir())
            except (PermissionError, OSError) as e:
                all_files_errors = f"Cannot access root {self.root}: {e}"
                return

            for entry in root_entries:
                if self._stop_event.is_set():
                    break
                try:
                    if entry.is_file():
                        self._process_file(entry, all_files)
                    elif entry.is_dir():
                        if self._should_scan_folder(entry, 1):
                            futures.append(executor.submit(self._collect_files, entry, 2, all_files))
                except (PermissionError, OSError):
                    continue

            for future in as_completed(futures):
                try:
                    future.result()
                except Exception:
                    pass

    def scan(self) -> ScanResult:
        start_time = time.time()

        all_files: List[FileInfo] = []
        self._scanned_count = 0

        self._run_scan(all_files)

        result = ScanResult(files=all_files)
        result.scan_duration = time.time() - start_time
        return result

    def scan_with_progress(self) -> ScanResult:
        start_time = time.time()

        all_files: List[FileInfo] = []
        self._scanned_count = 0

        with tqdm(total=None, desc="Scanning", unit=" files", bar_format="{l_bar}{bar}| {n_fmt} files") as pbar:
            def update_progress(current, total):
                pbar.n = current
                pbar.refresh()

            self.progress_callback = update_progress
            self._run_scan(all_files)
            pbar.n = self._scanned_count
            pbar.close()

        result = ScanResult(files=all_files)
        result.scan_duration = time.time() - start_time
        return result