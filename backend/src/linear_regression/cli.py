"""Command-line interface for linear_regression package."""

import argparse
import logging
import sys
from pathlib import Path

from .config import AppConfig, LogLevel
from .data_loader import load_csv
from .exceptions import LinearRegressionError
from .model import fit_linear_regression
from .plotting import generate_plot


def _setup_logging(config: AppConfig) -> None:
    level = getattr(logging, config.logging.level.value)
    fmt = config.logging.format_string
    logging.basicConfig(level=level, format=fmt, datefmt=config.logging.date_format)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Calculate and visualize linear regression from CSV data.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "file_path",
        nargs="?",
        help="Path to CSV file with x,y columns (default: uses config default)",
    )
    parser.add_argument(
        "--output", "-o",
        dest="output_path",
        type=Path,
        help="Save plot to file instead of displaying"
    )
    parser.add_argument(
        "--config", "-c",
        dest="config_path",
        type=Path,
        help="Path to YAML configuration file"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose (DEBUG) logging"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress console output"
    )
    parser.add_argument(
        "--precision",
        type=int,
        default=None,
        help="Decimal precision for output (default: from config)"
    )
    return parser


def run(
    file_path: Path | str | None = None,
    output_path: Path | str | None = None,
    config: AppConfig | None = None,
) -> int:
    """
    Run the regression analysis.

    Args:
        file_path: Input CSV path.
        output_path: Optional output path for plot.
        config: Application configuration.

    Returns:
        Exit code (0 for success, >0 for error).
    """
    cfg = config or AppConfig()
    logger = logging.getLogger("linear_regression.cli")

    input_path = Path(file_path) if file_path else cfg.default_csv_path

    try:
        dataset = load_csv(input_path, cfg.data)
        result = fit_linear_regression(
            dataset.x_values, dataset.y_values, cfg.regression
        )

        logger.info("Loaded %d points, computed regression successfully.", dataset.size)

        if not cfg.logging.use_console:
            print(result.equation(cfg.regression.regression_precision))

        generate_plot(
            list(dataset.x_values),
            list(dataset.y_values),
            result,
            output_path,
            cfg.plotting,
        )

        logger.info("Analysis complete.")
        return 0

    except LinearRegressionError as exc:
        logger.error("%s", exc.message)
        return exc.exit_code


def main() -> int:
    """CLI entry point."""
    parser = _build_parser()
    args = parser.parse_args()

    config = AppConfig()
    if args.verbose:
        config.logging.level = LogLevel.DEBUG
    if args.quiet:
        config.logging.use_console = False

    _setup_logging(config)

    return run(args.file_path, args.output_path, config)


if __name__ == "__main__":
    sys.exit(main())