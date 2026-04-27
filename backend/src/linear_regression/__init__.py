"""Linear regression analysis with CSV input and visualization.

Public API:
    load_csv: Load data from CSV file.
    fit_linear_regression: Calculate regression coefficients.
    generate_plot: Create visualization.
    RegressionResult: Result container.
    DataSet: Dataset container.
    DataPoint: Single data point.
    AppConfig: Main configuration.
    DEFAULT_CONFIG: Default settings.

Exceptions:
    LinearRegressionError: Base exception.
    DataLoadError: Data loading errors.
    ModelError: Model calculation errors.
    PlottingError: Plot generation errors.
"""

from .config import (
    AppConfig,
    DEFAULT_CONFIG,
    PlotConfig,
    PolynomialConfig,
    RegressionConfig,
)
from .data_loader import DataPoint, DataSet, load_csv
from .exceptions import (
    DataLoadError,
    DegenerateDataError,
    DimensionMismatchError,
    EmptyDataError,
    FileNotFoundError,
    InsufficientDataError,
    LinearRegressionError,
    ModelError,
    OutputWriteError,
    PlottingError,
    ValidationError,
)
from .model import (
    PolynomialResult,
    RegressionResult,
    fit_linear_regression,
    fit_polynomial,
)
from .plotting import generate_combined_plot, generate_plot, generate_polynomial_plot

__all__ = [
    "load_csv",
    "fit_linear_regression",
    "fit_polynomial",
    "generate_plot",
    "generate_polynomial_plot",
    "generate_combined_plot",
    "RegressionResult",
    "PolynomialResult",
    "DataSet",
    "DataPoint",
    "AppConfig",
    "DEFAULT_CONFIG",
    "LinearRegressionError",
    "DataLoadError",
    "FileNotFoundError",
    "EmptyDataError",
    "ValidationError",
    "InsufficientDataError",
    "ModelError",
    "DegenerateDataError",
    "DimensionMismatchError",
    "PlottingError",
    "OutputWriteError",
    "PlotConfig",
    "PolynomialConfig",
    "RegressionConfig",
]
__version__ = "2.1.0"