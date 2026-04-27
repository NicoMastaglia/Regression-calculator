"""Plotting functionality for linear_regression package."""

import logging
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from .config import PlotConfig
from .exceptions import OutputWriteError, PlottingError
from .model import PolynomialResult, RegressionResult

LOGGER = logging.getLogger(__name__)


def generate_plot(
    x: list[float],
    y: list[float],
    result: RegressionResult,
    output_path: Path | str | None = None,
    config: PlotConfig | None = None,
) -> None:
    """
    Generate and display or save regression plot.

    Args:
        x: X values from dataset.
        y: Y values from dataset.
        result: RegressionResult containing slope and intercept.
        output_path: Optional path to save plot (PNG/PDF).
        config: Optional plotting configuration.

    Raises:
        PlottingError: If plot generation fails.
        OutputWriteError: If file cannot be written.
    """
    if not x or not y:
        raise PlottingError("Cannot generate plot without data.")

    cfg = config or PlotConfig()

    plt.figure(figsize=cfg.figsize)
    plt.scatter(x, y, color=cfg.scatter_color, label=cfg.scatter_label,
               s=cfg.scatter_size, alpha=cfg.scatter_alpha)

    x_min, x_max = min(x), max(x)
    x_line = np.linspace(x_min, x_max, 100)
    y_line = result.slope * x_line + result.intercept

    r_sq_text = f", R²={result.r_squared:.4f}" if result.r_squared is not None else ""
    equation_label = f"Regression: y = {result.slope:.4f}x + {result.intercept:.4f}{r_sq_text}"

    plt.plot(x_line, y_line, color=cfg.regression_color,
             linewidth=cfg.regression_width, label=equation_label)

    plt.xlabel(cfg.xlabel)
    plt.ylabel(cfg.ylabel)
    plt.title(cfg.title)
    plt.legend()
    plt.grid(True, alpha=cfg.grid_alpha)

    try:
        if output_path:
            save_path = Path(output_path)
            plt.savefig(save_path, bbox_inches="tight")
            LOGGER.info("Plot saved to: %s", save_path)
        else:
            plt.show()
    except Exception as exc:
        raise OutputWriteError(str(output_path or "display"), str(exc)) from exc
    finally:
        plt.close()


def generate_polynomial_plot(
    x: list[float],
    y: list[float],
    result: PolynomialResult,
    output_path: Path | str | None = None,
    config: PlotConfig | None = None,
) -> None:
    """
    Generate and display or save polynomial regression plot.

    Args:
        x: X values from dataset.
        y: Y values from dataset.
        result: PolynomialResult containing coefficients.
        output_path: Optional path to save plot (PNG/PDF).
        config: Optional plotting configuration.

    Raises:
        PlottingError: If plot generation fails.
        OutputWriteError: If file cannot be written.
    """
    if not x or not y:
        raise PlottingError("Cannot generate plot without data.")

    cfg = config or PlotConfig()

    plt.figure(figsize=cfg.figsize)
    plt.scatter(x, y, color=cfg.scatter_color, label=cfg.scatter_label,
               s=cfg.scatter_size, alpha=cfg.scatter_alpha)

    x_min, x_max = min(x), max(x)
    x_line = np.linspace(x_min, x_max, 100)

    coeffs = list(result.coefficients)
    y_line = np.polyval(coeffs, x_line)

    r_sq_text = f", R²={result.r_squared:.4f}" if result.r_squared is not None else ""
    degree = len(coeffs) - 1
    equation_label = f"Polynomial (degree {degree}): {result.equation()}{r_sq_text}"

    plt.plot(x_line, y_line, color=cfg.regression_color,
             linewidth=cfg.regression_width, label=equation_label)

    plt.xlabel(cfg.xlabel)
    plt.ylabel(cfg.ylabel)
    plt.title(cfg.title)
    plt.legend()
    plt.grid(True, alpha=cfg.grid_alpha)

    try:
        if output_path:
            save_path = Path(output_path)
            plt.savefig(save_path, bbox_inches="tight")
            LOGGER.info("Polynomial plot saved to: %s", save_path)
        else:
            plt.show()
    except Exception as exc:
        raise OutputWriteError(str(output_path or "display"), str(exc)) from exc
    finally:
        plt.close()


def generate_combined_plot(
    x: list[float],
    y: list[float],
    linear_result: RegressionResult,
    polynomial_result: PolynomialResult,
    output_path: Path | str | None = None,
    config: PlotConfig | None = None,
) -> None:
    """
    Generate plot with both linear and polynomial regression curves.

    Args:
        x: X values from dataset.
        y: Y values from dataset.
        linear_result: Linear RegressionResult.
        polynomial_result: Polynomial result.
        output_path: Optional path to save plot (PNG/PDF).
        config: Optional plotting configuration.

    Raises:
        PlottingError: If plot generation fails.
        OutputWriteError: If file cannot be written.
    """
    if not x or not y:
        raise PlottingError("Cannot generate plot without data.")

    cfg = config or PlotConfig()

    plt.figure(figsize=cfg.figsize)
    plt.scatter(
        x, y,
        color=cfg.scatter_color,
        label=cfg.scatter_label,
        s=cfg.scatter_size,
        alpha=cfg.scatter_alpha,
    )

    x_min, x_max = min(x), max(x)
    x_line = np.linspace(x_min, x_max, 100)

    y_linear = linear_result.slope * x_line + linear_result.intercept
    r_sq_linear = f", R²={linear_result.r_squared:.4f}" if linear_result.r_squared else ""
    plt.plot(
        x_line,
        y_linear,
        color="red",
        linewidth=cfg.regression_width,
        linestyle="--",
        label=f"Linear: y = {linear_result.slope:.4f}x + {linear_result.intercept:.4f}{r_sq_linear}",
    )

    poly_coeffs = list(polynomial_result.coefficients)
    y_poly = np.polyval(poly_coeffs, x_line)
    degree = len(poly_coeffs) - 1
    r_sq_poly = f", R²={polynomial_result.r_squared:.4f}" if polynomial_result.r_squared else ""
    plt.plot(
        x_line,
        y_poly,
        color="green",
        linewidth=cfg.regression_width,
        label=f"Polynomial (degree {degree}): {polynomial_result.equation()}{r_sq_poly}",
    )

    plt.xlabel(cfg_xlabel := cfg.xlabel)
    plt.ylabel(cfg.ylabel)
    plt.title("Linear vs Polynomial Regression")
    plt.legend(loc="upper left")
    plt.grid(True, alpha=cfg.grid_alpha)

    try:
        if output_path:
            save_path = Path(output_path)
            plt.savefig(save_path, bbox_inches="tight")
            LOGGER.info("Combined plot saved to: %s", save_path)
        else:
            plt.show()
    except Exception as exc:
        raise OutputWriteError(str(output_path or "display"), str(exc)) from exc
    finally:
        plt.close()