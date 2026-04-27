"""REST API for linear and polynomial regression."""

from __future__ import annotations

import csv
import io
import logging
from typing import Any

from fastapi import Body, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, model_validator

from src.linear_regression import (
    DEFAULT_CONFIG,
    fit_linear_regression,
    fit_polynomial,
)
from src.linear_regression.exceptions import LinearRegressionError

LOGGER = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

app = FastAPI(title="Regression API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PointsRequest(BaseModel):
    """Request payload for regression from x/y arrays."""

    x: list[float] = Field(..., min_length=2)
    y: list[float] = Field(..., min_length=2)
    degree: int = Field(default=2, ge=1)

    @model_validator(mode="after")
    def validate_lengths(self) -> "PointsRequest":
        if len(self.x) != len(self.y):
            raise ValueError("x e y devono avere la stessa lunghezza")
        return self


class RegressionResponse(BaseModel):
    """Standard API response for regressions."""

    points_count: int
    x: list[float]
    y: list[float]
    linear: dict[str, Any]
    polynomial: dict[str, Any]


def _build_regression_response(
    x_values: list[float],
    y_values: list[float],
    degree: int,
) -> RegressionResponse:
    linear_result = fit_linear_regression(
        x_values,
        y_values,
        config=DEFAULT_CONFIG.regression,
    )
    polynomial_result = fit_polynomial(
        x_values,
        y_values,
        degree=degree,
        config=DEFAULT_CONFIG.polynomial,
    )

    return RegressionResponse(
        points_count=len(x_values),
        x=x_values,
        y=y_values,
        linear={
            "m": linear_result.slope,
            "q": linear_result.intercept,
            "r_squared": linear_result.r_squared,
            "equation": linear_result.equation(),
        },
        polynomial={
            "degree": degree,
            "coefficients": list(polynomial_result.coefficients),
            "r_squared": polynomial_result.r_squared,
            "equation": polynomial_result.equation(),
        },
    )


def _parse_csv_binary(content: bytes) -> tuple[list[float], list[float]]:
    if not content:
        raise ValueError("Body binario CSV vuoto")

    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("CSV non valido: usare UTF-8") from exc

    reader = csv.reader(io.StringIO(text))
    rows = [row for row in reader if row and any(cell.strip() for cell in row)]
    if not rows:
        raise ValueError("CSV vuoto")

    x_values: list[float] = []
    y_values: list[float] = []

    start_index = 0
    try:
        float(rows[0][0])
        float(rows[0][1])
    except (ValueError, IndexError):
        start_index = 1

    for index, row in enumerate(rows[start_index:], start=start_index + 1):
        if len(row) < 2:
            raise ValueError(f"Riga {index} non valida: servono almeno 2 colonne")
        try:
            x_values.append(float(row[0].strip()))
            y_values.append(float(row[1].strip()))
        except ValueError as exc:
            raise ValueError(f"Valori non numerici alla riga {index}") from exc

    if len(x_values) < 2:
        raise ValueError("Servono almeno 2 punti validi")

    return x_values, y_values


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Regression API is running"}


@app.post("/regression/points", response_model=RegressionResponse)
def regression_from_points(payload: PointsRequest) -> RegressionResponse:
    """Compute linear and polynomial regression from JSON arrays x/y."""
    try:
        response = _build_regression_response(payload.x, payload.y, payload.degree)
        LOGGER.info("/regression/points processed with %d points", response.points_count)
        return response
    except (LinearRegressionError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/regression/csv", response_model=RegressionResponse)
def regression_from_binary_csv(
    csv_file: bytes = Body(..., media_type="application/octet-stream"),
    degree: int = 2,
) -> RegressionResponse:
    """Compute linear and polynomial regression from binary CSV body."""
    if degree < 1:
        raise HTTPException(status_code=400, detail="degree deve essere >= 1")

    try:
        x_values, y_values = _parse_csv_binary(csv_file)
        response = _build_regression_response(x_values, y_values, degree)
        LOGGER.info("/regression/csv processed with %d points", response.points_count)
        return response
    except (LinearRegressionError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
