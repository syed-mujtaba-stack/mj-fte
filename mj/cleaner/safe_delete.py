import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional, Callable
from enum import Enum
from send2trash import send2trash
import win32file
import win32con

from mj.config.settings import settings
from mj.analyzer.windows_rules import WindowsRules
from mj.analyzer.classifier import FileClassification, FileCategory


class CleanAction(Enum):
    DELETE = "delete"
    SKIP = "skip"
    QUARANTINE = "quarantine"


@dataclass
class CleanResult:
    file: Path
    action: CleanAction
    success: bool
    error: str = ""
    size_freed: int = 0


class SafeCleaner:
    def __init__(
        self,
        use_recycle_bin: bool = None,
        confirm_each: bool = None,
        dry_run: bool = None,
        progress_callback: Optional[Callable[[int, int, Path], None]] = None,
    ):
        self.use_recycle_bin = use_recycle_bin if use_recycle_bin is not None else settings.use_recycle_bin
        self.confirm_each = confirm_each if confirm_each is not None else settings.confirm_each_file
        self.dry_run = dry_run if dry_run is not None else settings.dry_run_default
        self.progress_callback = progress_callback
        self.windows_rules = WindowsRules()
        self._stop_event = False

    def stop(self):
        self._stop_event = True

    def clean(
        self,
        classifications: List[FileClassification],
        categories: List[FileCategory] = None,
        confirm_callback: Optional[Callable[[FileClassification], CleanAction]] = None,
    ) -> List[CleanResult]:
        if categories is None:
            categories = [FileCategory.JUNK, FileCategory.DANGEROUS]

        actionable = [
            c for c in classifications
            if c.category in categories and c.is_actionable
        ]

        results = []
        total = len(actionable)

        for i, classification in enumerate(actionable):
            if self._stop_event:
                break

            if self.progress_callback:
                self.progress_callback(i + 1, total, classification.file.path)

            action = CleanAction.SKIP

            if self.dry_run:
                action = CleanAction.DELETE
            elif self.confirm_each and confirm_callback:
                action = confirm_callback(classification)
            elif not self.confirm_each:
                action = CleanAction.DELETE

            if action == CleanAction.DELETE:
                result = self._delete_file(classification.file)
            else:
                result = CleanResult(
                    file=classification.file.path,
                    action=action,
                    success=True,
                    error="" if action == CleanAction.SKIP else "Quarantine not implemented",
                )

            results.append(result)

        return results

    def _delete_file(self, file_info) -> CleanResult:
        path = file_info.path

        if self.windows_rules.is_windows_file(path):
            return CleanResult(
                file=path,
                action=CleanAction.SKIP,
                success=False,
                error="File is protected by Windows rules",
            )

        try:
            size = file_info.size

            if self.dry_run:
                return CleanResult(
                    file=path,
                    action=CleanAction.DELETE,
                    success=True,
                    error="(dry run)",
                    size_freed=size,
                )

            if self.use_recycle_bin:
                send2trash(str(path))
            else:
                try:
                    attrs = win32file.GetFileAttributes(str(path))
                    if attrs & win32con.FILE_ATTRIBUTE_READONLY:
                        win32file.SetFileAttributes(str(path), attrs & ~win32con.FILE_ATTRIBUTE_READONLY)
                except Exception:
                    pass
                path.unlink()

            return CleanResult(
                file=path,
                action=CleanAction.DELETE,
                success=True,
                error="",
                size_freed=size,
            )

        except PermissionError:
            return CleanResult(
                file=path,
                action=CleanAction.SKIP,
                success=False,
                error="Permission denied",
            )
        except FileNotFoundError:
            return CleanResult(
                file=path,
                action=CleanAction.SKIP,
                success=False,
                error="File not found",
            )
        except Exception as e:
            return CleanResult(
                file=path,
                action=CleanAction.SKIP,
                success=False,
                error=str(e),
            )

    def get_summary(self, results: List[CleanResult]) -> dict:
        deleted = [r for r in results if r.action == CleanAction.DELETE and r.success]
        skipped = [r for r in results if r.action == CleanAction.SKIP]
        failed = [r for r in results if not r.success and r.action != CleanAction.SKIP]

        return {
            "total": len(results),
            "deleted": len(deleted),
            "skipped": len(skipped),
            "failed": len(failed),
            "space_freed": sum(r.size_freed for r in deleted),
            "errors": [r.error for r in failed if r.error],
        }