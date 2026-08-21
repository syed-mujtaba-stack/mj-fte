import os
from pathlib import Path
from typing import Set, List, Optional
import win32file
import win32con

from mj.config.settings import settings


class WindowsRules:
    def __init__(self):
        self._protected_paths: Set[Path] = set()
        self._protected_folder_prefixes: List[str] = []
        self._initialize_protected_paths()

    def _initialize_protected_paths(self):
        for path_str in settings.windows_protected_paths:
            try:
                path = Path(path_str).resolve()
                if path.exists():
                    self._protected_paths.add(path)
            except Exception:
                pass

        user_profile = os.getenv("USERPROFILE", str(Path.home()))
        self._protected_folder_prefixes = [
            os.path.normcase(str(Path(user_profile) / folder))
            for folder in settings.user_protected_folders
        ]

    def is_protected_path(self, path: Path) -> bool:
        try:
            resolved = path.resolve()
            for protected in self._protected_paths:
                try:
                    resolved.relative_to(protected)
                    return True
                except ValueError:
                    continue
        except Exception:
            pass
        return False

    def is_protected_folder(self, path: Path) -> bool:
        try:
            norm = os.path.normcase(str(path.resolve()))
            for prefix in self._protected_folder_prefixes:
                if norm == prefix or norm.startswith(prefix + os.sep):
                    return True
        except Exception:
            pass
        return False

    def has_protected_attributes(self, path: Path) -> bool:
        try:
            attrs = win32file.GetFileAttributes(str(path))
            if attrs & win32con.FILE_ATTRIBUTE_SYSTEM:
                return True
            if attrs & win32con.FILE_ATTRIBUTE_HIDDEN:
                return True
            if attrs & win32con.FILE_ATTRIBUTE_READONLY:
                return True
        except Exception:
            pass
        return False

    def is_windows_file(self, path: Path) -> bool:
        return (
            self.is_protected_path(path)
            or self.is_protected_folder(path)
            or self.has_protected_attributes(path)
        )

    def get_protected_reason(self, path: Path) -> Optional[str]:
        try:
            resolved = path.resolve()
            for protected in self._protected_paths:
                try:
                    resolved.relative_to(protected)
                    return f"Inside protected system path: {protected}"
                except ValueError:
                    continue
        except Exception:
            pass

        try:
            norm = os.path.normcase(str(path.resolve()))
            for prefix in self._protected_folder_prefixes:
                if norm == prefix or norm.startswith(prefix + os.sep):
                    return f"Inside protected user folder: {prefix}"
        except Exception:
            pass

        try:
            attrs = win32file.GetFileAttributes(str(path))
            if attrs & win32con.FILE_ATTRIBUTE_SYSTEM:
                return "Has SYSTEM attribute"
            if attrs & win32con.FILE_ATTRIBUTE_HIDDEN:
                return "Has HIDDEN attribute"
            if attrs & win32con.FILE_ATTRIBUTE_READONLY:
                return "Has READONLY attribute"
        except Exception:
            pass

        return None