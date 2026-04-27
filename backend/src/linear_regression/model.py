"""Linear regression model implementation."""

import logging
from dataclasses import dataclass
from typing import Iterable

import numpy as np

from .config import PolynomialConfig, RegressionConfig
from .exceptions import DegenerateDataError, DimensionMismatchError, ModelError

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class RegressionResult:
    """Result of linear regression calculation."""

    slope: float
    intercept: float
    r_squared: float | None = None

    def equation(self, precision: int = 4) -> str:
        return f"y = {self.slope:.{precision}f}x + {self.intercept:.{precision}f}"


def _calculate_r_squared(
    x_values: list[float], y_values: list[float], m: float, q: float
) -> float | None:
    if len(x_values) < 3:
        return None

    n = len(x_values)
    y_mean = sum(y_values) / n

    ss_tot = sum((y_i - y_mean) ** 2 for y_i in y_values)
    if ss_tot == 0:
        return None

    ss_res = sum((y_i - (m * x_i + q)) ** 2 for x_i, y_i in zip(x_values, y_values))
    return 1 - (ss_res / ss_tot)


def fit_linear_regression(
    x: Iterable[float],
    y: Iterable[float],
    config: RegressionConfig | None = None,
) -> RegressionResult:
    """
    Calculate linear regression coefficients (y = mx + q).

    Args:
        x: Iterable of x values.
        y: Iterable of y values.
        config: Optional configuration.

    Returns:
        RegressionResult with slope (m), intercept (q), and R².

    Raises:
        DimensionMismatchError: If x and y have different lengths.
        ModelError: If fewer than 2 points provided.
        DegenerateDataError: If denominator is zero.
    """
    cfg = config or RegressionConfig()
    x_values = list(x)
    y_values = list(y)

    x_len = len(x_values)
    y_len = len(y_values)

    if x_len != y_len:
        raise DimensionMismatchError(x_len, y_len)

    if x_len < cfg.min_points:
        raise ModelError(
            f"Need at least {cfg.min_points} points for regression, got {x_len}."
        )

    n = x_len
    sum_x = sum(x_values)
    sum_y = sum(y_values)
    sum_xy = sum(x_i * y_i for x_i, y_i in zip(x_values, y_values))
    sum_x2 = sum(x_i**2 for x_i in x_values)

    denominator = n * sum_x2 - sum_x**2

    if denominator == 0:
        raise DegenerateDataError("all x values are identical.")

    m = (n * sum_xy - sum_x * sum_y) / denominator
    q = (sum_y - m * sum_x) / n

    r_squared = _calculate_r_squared(x_values, y_values, m, q)

    LOGGER.debug(
        "Regression: m=%.6f, q=%.6f, R²=%.4f", m, q, r_squared or float("nan")
    )

    return RegressionResult(slope=m, intercept=q, r_squared=r_squared)


@dataclass(frozen=True, slots=True)
class PolynomialResult:
    """Result of polynomial regression calculation."""

    coefficients: tuple[float, ...]
    r_squared: float | None = None

    def equation(self, precision: int = 4) -> str:
        terms = []
        degree = len(self.coefficients) - 1
        for i, coef in enumerate(self.coefficients):
            power = degree - i
            if power == 0:
                terms.append(f"{coef:.{precision}f}")
            elif power == 1:
                terms.append(f"{coef:.{precision}f}x")
            else:
                terms.append(f"{coef:.{precision}f}x^{power}")
        return "y = " + " + ".join(terms)


def fit_polynomial(
    x: Iterable[float],
    y: Iterable[float],
    degree: int = 2,
    config: PolynomialConfig | None = None,
) -> PolynomialResult:
    """
    Calculate polynomial regression coefficients using numpy polyfit.

    Args:
        x: Iterable of x values.
        y: Iterable of y values.
        degree: Degree of polynomial (default: 2).
        config: Optional configuration.

    Returns:
        PolynomialResult with coefficients and R².

    Raises:
        DimensionMismatchError: If x and y have different lengths.
        ModelError: If not enough points for the degree.
    """
    cfg = config or PolynomialConfig()
    x_values = np.array(list(x))
    y_values = np.array(list(y))

    x_len = len(x_values)
    y_len = len(y_values)

    if x_len != y_len:
        raise DimensionMismatchError(x_len, y_len)

    effective_degree = degree if degree > 0 else cfg.degree
    min_required = effective_degree + 1 if effective_degree > 0 else 2
    if x_len < min_required:
        raise ModelError(
            f"Need at least {min_required} points for degree {effective_degree} polynomial, got {x_len}."
        )

    try:
        coeffs = np.polyfit(x_values, y_values, effective_degree)
    except np.linalg.LinAlgError as exc:
        raise DegenerateDataError(f"singular matrix: {exc}") from exc

    poly = np.poly1d(coeffs)
    y_pred = poly(x_values)

    if len(x_values) > degree + 1:
        ss_tot = np.sum((y_values - np.mean(y_values)) ** 2)
        ss_res = np.sum((y_values - y_pred) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else None
    else:
        r_squared = None

    LOGGER.debug(
        "Polynomial degree %d: coeffs=%s, R²=%.4f",
        degree,
        coeffs,
        r_squared or float("nan"),
    )

    return PolynomialResult(
        coefficients=tuple(coeffs.tolist()),
        r_squared=r_squared,
    )