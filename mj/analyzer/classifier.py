from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Set
import fnmatch

from mj.config.settings import settings
from mj.analyzer.scanner import FileInfo


class FileCategory(Enum):
    JUNK = "junk"
    DANGEROUS = "dangerous"
    PROTECTED = "protected"
    NORMAL = "normal"


@dataclass
class FileClassification:
    file: FileInfo
    category: FileCategory
    reasons: List[str]
    confidence: float

    @property
    def is_actionable(self) -> bool:
        return self.category in (FileCategory.JUNK, FileCategory.DANGEROUS) and not self.file.is_protected


class FileClassifier:
    def __init__(self):
        self.junk_extensions = settings.junk_extensions
        self.junk_folders = settings.junk_folders
        self.junk_patterns = settings.junk_file_patterns
        self.dangerous_extensions = settings.dangerous_extensions
        self.suspicious_names = settings.suspicious_names

    def classify(self, file_info: FileInfo) -> FileClassification:
        if file_info.is_protected:
            return FileClassification(
                file=file_info,
                category=FileCategory.PROTECTED,
                reasons=[file_info.classification_reason or "Protected by Windows rules"],
                confidence=1.0,
            )

        junk_reasons = self._check_junk(file_info)
        dangerous_reasons = self._check_dangerous(file_info)

        if junk_reasons and dangerous_reasons:
            if len(dangerous_reasons) > len(junk_reasons):
                return FileClassification(
                    file=file_info,
                    category=FileCategory.DANGEROUS,
                    reasons=dangerous_reasons,
                    confidence=0.8,
                )
            else:
                return FileClassification(
                    file=file_info,
                    category=FileCategory.JUNK,
                    reasons=junk_reasons,
                    confidence=0.7,
                )
        elif dangerous_reasons:
            return FileClassification(
                file=file_info,
                category=FileCategory.DANGEROUS,
                reasons=dangerous_reasons,
                confidence=0.9,
            )
        elif junk_reasons:
            return FileClassification(
                file=file_info,
                category=FileCategory.JUNK,
                reasons=junk_reasons,
                confidence=0.8,
            )
        else:
            return FileClassification(
                file=file_info,
                category=FileCategory.NORMAL,
                reasons=[],
                confidence=0.0,
            )

    def _check_junk(self, file_info: FileInfo) -> List[str]:
        reasons = []

        if file_info.extension in self.junk_extensions:
            reasons.append(f"Junk extension: {file_info.extension}")

        folder_name = Path(file_info.folder).name.lower()
        if folder_name in self.junk_folders:
            reasons.append(f"In junk folder: {folder_name}")

        for pattern in self.junk_patterns:
            if fnmatch.fnmatch(file_info.path.name.lower(), pattern.lower()):
                reasons.append(f"Matches junk pattern: {pattern}")
                break

        return reasons

    def _check_dangerous(self, file_info: FileInfo) -> List[str]:
        reasons = []

        if file_info.extension in self.dangerous_extensions:
            reasons.append(f"Dangerous extension: {file_info.extension}")

            name_lower = file_info.path.stem.lower()
            for suspicious in self.suspicious_names:
                if suspicious in name_lower:
                    reasons.append(f"Suspicious name contains: {suspicious}")
                    break

        return reasons

    def classify_batch(self, files: List[FileInfo]) -> List[FileClassification]:
        return [self.classify(f) for f in files]