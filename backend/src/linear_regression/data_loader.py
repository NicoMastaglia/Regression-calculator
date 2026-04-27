"""Data loading and validation for linear_regression package."""

import csv
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

from .config import DataConfig
from .exceptions import (
    EmptyDataError,
    FileNotFoundError,
    InsufficientDataError,
    ValidationError,
)

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class DataPoint:
    """A single data point with x and y coordinates."""

    x: float
    y: float
    row: int


@dataclass(frozen=True, slots=True)
class DataSet:
    """Container for loaded dataset."""

    points: tuple[DataPoint, ...]

    @property
    def x_values(self) -> tuple[float, ...]:
        return tuple(p.x for p in self.points)

    @property
    def y_values(self) -> tuple[float, ...]:
        return tuple(p.y for p in self.points)

    @property
    def size(self) -> int:
        return len(self.points)


def _is_empty_row(row: list[str]) -> bool:
    return all(cell.strip() == "" for cell in row)


def _parse_value(value: str, row: int) -> float:
    try:
        return float(value.strip())
    except ValueError as exc:
        raise ValidationError(
            f"Non-numeric value: {value!r}", row=row
        ) from exc


def _read_rows(path: Path, config: DataConfig) -> Iterator[tuple[int, list[str]]]:
    with path.open("r", newline="", encoding=config.default_encoding) as file:
        reader = csv.reader(file)
        for row_number, row in enumerate(reader, start=1):
            yield row_number, row


def load_csv(file_path: Path | str, config: DataConfig | None = None) -> DataSet:
    """
    Load data from CSV file.

    Args:
        file_path: Path to CSV file.
        config: Optional configuration for data loading.

    Returns:
        DataSet containing all valid data points.

    Raises:
        FileNotFoundError: If file does not exist.
        EmptyDataError: If file is empty.
        InsufficientDataError: If fewer than 2 valid points.
    """
    cfg = config or DataConfig()
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(str(path))

    rows_iter = _read_rows(path, cfg)
    row_number = 0
    points: list[DataPoint] = []

    for row_number, row in rows_iter:
        if cfg.has_header and row_number == 1:
            continue

        if cfg.skip_empty_rows and _is_empty_row(row):
            continue

        if len(row) < cfg.min_columns:
            raise ValidationError(
                f"Row has fewer than {cfg.min_columns} columns", row=row_number
            )

        try:
            x = _parse_value(row[0], row_number)
            y = _parse_value(row[1], row_number)
            points.append(DataPoint(x=x, y=y, row=row_number))
        except ValidationError:
            if cfg.skip_empty_rows and _is_row_empty_validation(row):
                continue
            raise

    if not points:
        raise EmptyDataError("file")

    if len(points) < cfg.min_columns:
        raise InsufficientDataError(required=cfg.min_columns, found=len(points))

    LOGGER.info("Loaded %d valid data points from CSV.", len(points))
    return DataSet(points=tuple(points))


def _is_row_empty_validation(row: list[str]) -> bool:
    try:
        for cell in row[:2]:
            _ = _parse_value(cell, 0)
        return False
    except ValidationError:
        return True