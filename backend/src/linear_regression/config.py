"""Configuration for linear_regression package."""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


@dataclass(frozen=True)
class PlotConfig:
    """Configuration for plot generation."""

    figsize: tuple[float, float] = (10, 6)
    scatter_color: str = "blue"
    scatter_label: str = "CSV Data"
    scatter_size: int = 50
    scatter_alpha: float = 0.7
    regression_color: str = "red"
    regression_width: float = 2.0
    grid_alpha: float = 0.3
    xlabel: str = "X"
    ylabel: str = "Y"
    title: str = "Linear Regression"


@dataclass(frozen=True)
class RegressionConfig:
    """Configuration for regression calculation."""

    min_points: int = 2
    regression_precision: int = 4
    output_precision: int = 6


@dataclass(frozen=True)
class PolynomialConfig:
    """Configuration for polynomial regression."""

    degree: int = 2
    min_points: int = 3


@dataclass(frozen=True)
class DataConfig:
    """Configuration for data loading."""

    default_encoding: str = "utf-8"
    skip_empty_rows: bool = True
    min_columns: int = 2
    has_header: bool = True


@dataclass(frozen=True)
class LogConfig:
    """Configuration for logging."""

    level: LogLevel = LogLevel.INFO
    format_string: str = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    date_format: str = "%Y-%m-%d %H:%M:%S"
    use_console: bool = True


@dataclass(frozen=True)
class AppConfig:
    """Main application configuration."""

    regression: RegressionConfig = RegressionConfig()
    polynomial: PolynomialConfig = PolynomialConfig()
    plotting: PlotConfig = PlotConfig()
    data: DataConfig = DataConfig()
    logging: LogConfig = LogConfig()
    default_csv_path: Path = Path("dati.csv")


DEFAULT_CONFIG = AppConfig()