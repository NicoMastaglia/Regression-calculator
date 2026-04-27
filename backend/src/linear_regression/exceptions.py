"""Custom exceptions for linear_regression package."""


class LinearRegressionError(Exception):
    """Base exception for all linear_regression errors."""

    exit_code: int = 1

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class DataLoadError(LinearRegressionError):
    """Raised when data loading or parsing fails."""

    exit_code = 2


class FileNotFoundError(DataLoadError):
    """Raised when input file does not exist."""

    exit_code = 2

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        super().__init__(f"File not found: {file_path}")
        self.message = f"File not found: {file_path}"


class EmptyDataError(DataLoadError):
    """Raised when data source is empty."""

    exit_code = 3

    def __init__(self, source: str = "file") -> None:
        super().__init__(f"The {source} is empty.")


class ValidationError(DataLoadError):
    """Raised when data validation fails."""

    exit_code = 3

    def __init__(self, message: str, row: int | None = None) -> None:
        self.row = row
        location = f" at row {row}" if row else ""
        super().__init__(f"{message}{location}")


class InsufficientDataError(DataLoadError):
    """Raised when not enough valid data points."""

    exit_code = 3

    def __init__(self, required: int, found: int) -> None:
        super().__init__(
            f"Need at least {required} valid points for regression, found {found}."
        )


class ModelError(LinearRegressionError):
    """Raised when regression calculation fails."""

    exit_code = 4


class DegenerateDataError(ModelError):
    """Raised when data produces degenerate solution (e.g., all x values identical)."""

    exit_code = 4

    def __init__(self, reason: str) -> None:
        super().__init__(f"Cannot compute regression: {reason}.")


class DimensionMismatchError(ModelError):
    """Raised when x and y have different lengths."""

    exit_code = 4

    def __init__(self, x_len: int, y_len: int) -> None:
        super().__init__(f"Length mismatch: x has {x_len} points, y has {y_len}.")


class PlottingError(LinearRegressionError):
    """Raised when plot generation fails."""

    exit_code = 5


class OutputWriteError(PlottingError):
    """Raised when output file cannot be written."""

    exit_code = 5

    def __init__(self, file_path: str, reason: str) -> None:
        super().__init__(f"Cannot write output to {file_path}: {reason}")