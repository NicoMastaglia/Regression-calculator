import { useMemo, useState } from "react";
import {
  Chart as ChartJS,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Scatter } from "react-chartjs-2";

ChartJS.register(
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
);

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";
const INITIAL_POINTS = [
  { x: "-3", y: "8.2" },
  { x: "-2", y: "3.6" },
  { x: "-1", y: "1.1" },
  { x: "0", y: "0.2" },
  { x: "1", y: "1.3" },
  { x: "2", y: "4" },
  { x: "3", y: "8.8" },
  { x: "4", y: "15.9" },
];

const LINEAR_SAMPLE = [
  { x: "1", y: "2" },
  { x: "2", y: "4" },
  { x: "3", y: "6" },
  { x: "4", y: "8" },
  { x: "5", y: "10" },
];

function evalPolynomial(coefficients, xValue) {
  return coefficients.reduce(
    (accumulator, coefficient) => accumulator * xValue + coefficient,
    0,
  );
}

function parsePoints(rows) {
  if (rows.length < 2) {
    throw new Error("Servono almeno 2 punti.");
  }

  const x = [];
  const y = [];
  rows.forEach((row, index) => {
    const parsedX = Number(row.x);
    const parsedY = Number(row.y);
    if (Number.isNaN(parsedX) || Number.isNaN(parsedY)) {
      throw new Error(`Valori non numerici alla riga ${index + 1}.`);
    }
    x.push(parsedX);
    y.push(parsedY);
  });

  return { x, y };
}

export default function App() {
  const [mode, setMode] = useState("manual");
  const [degree, setDegree] = useState(2);
  const [points, setPoints] = useState(INITIAL_POINTS);
  const [csvFile, setCsvFile] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const pointsCount =
    mode === "manual" ? points.length : (result?.points_count ?? 0);

  const chartData = useMemo(() => {
    if (!result) {
      return null;
    }

    const x = result.x;
    const y = result.y;
    const pointDataset = x.map((xValue, index) => ({ x: xValue, y: y[index] }));

    const minX = Math.min(...x);
    const maxX = Math.max(...x);
    const sampleCount = 140;
    const spread = maxX - minX || 1;
    const lineX = Array.from(
      { length: sampleCount },
      (_, index) => minX + (spread * index) / (sampleCount - 1),
    );

    const linearLine = lineX.map((xValue) => ({
      x: xValue,
      y: result.linear.m * xValue + result.linear.q,
    }));

    const polynomialLine = lineX.map((xValue) => ({
      x: xValue,
      y: evalPolynomial(result.polynomial.coefficients, xValue),
    }));

    return {
      datasets: [
        {
          label: "Osservazioni",
          data: pointDataset,
          pointRadius: 3.6,
          pointHoverRadius: 4.8,
          pointBackgroundColor: "#d5d7da",
          pointBorderColor: "#f2f2f2",
          pointBorderWidth: 0.8,
          showLine: false,
        },
        {
          label: "Lineare",
          data: linearLine,
          showLine: true,
          pointRadius: 0,
          borderColor: "#4ec5e8",
          borderDash: [6, 4],
          borderWidth: 2.1,
        },
        {
          label: `Polinomiale grado ${result.polynomial.degree}`,
          data: polynomialLine,
          showLine: true,
          pointRadius: 0,
          borderColor: "#e4a162",
          borderWidth: 2.2,
        },
      ],
    };
  }, [result]);

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: "bottom",
        align: "start",
        labels: {
          color: "#9aa8c2",
          boxWidth: 18,
          usePointStyle: true,
          pointStyle: "line",
        },
      },
      title: {
        display: false,
      },
      tooltip: {
        backgroundColor: "rgba(11, 17, 30, 0.96)",
        titleColor: "#f3f3f3",
        bodyColor: "#d2d8e5",
        borderColor: "rgba(70, 95, 139, 0.8)",
        borderWidth: 1,
      },
    },
    scales: {
      x: {
        type: "linear",
        title: { display: true, text: "x", color: "#707f9d" },
        ticks: { color: "#71809f", font: { size: 10 } },
        border: { color: "rgba(114, 127, 157, 0.55)" },
        grid: { color: "rgba(92, 110, 142, 0.2)" },
      },
      y: {
        title: { display: true, text: "y", color: "#707f9d" },
        ticks: { color: "#71809f", font: { size: 10 } },
        border: { color: "rgba(114, 127, 157, 0.55)" },
        grid: { color: "rgba(92, 110, 142, 0.2)" },
      },
    },
  };

  const updatePoint = (rowIndex, field, value) => {
    setPoints((previous) => {
      const next = [...previous];
      next[rowIndex] = { ...next[rowIndex], [field]: value };
      return next;
    });
  };

  const addRow = () => {
    setPoints((previous) => [...previous, { x: "0", y: "0" }]);
  };

  const removeRow = (rowIndex) => {
    setPoints((previous) => {
      if (previous.length <= 2) {
        setError("Devi mantenere almeno 2 punti.");
        return previous;
      }
      setError("");
      return previous.filter((_, index) => index !== rowIndex);
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setLoading(true);

    try {
      const degreeValue = Number(degree);
      if (!Number.isInteger(degreeValue) || degreeValue < 1) {
        throw new Error("Il grado deve essere un intero >= 1.");
      }

      let response;
      if (mode === "manual") {
        const { x, y } = parsePoints(points);

        response = await fetch(`${API_BASE_URL}/regression/points`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ x, y, degree: degreeValue }),
        });
      } else {
        if (!csvFile) {
          throw new Error("Seleziona un file CSV.");
        }

        const content = await csvFile.arrayBuffer();
        response = await fetch(
          `${API_BASE_URL}/regression/csv?degree=${degreeValue}`,
          {
            method: "POST",
            headers: { "Content-Type": "application/octet-stream" },
            body: content,
          },
        );
      }

      const payload = await response.json();
      if (!response.ok) {
        throw new Error(payload.detail || "Errore nella richiesta");
      }

      setResult(payload);
    } catch (submitError) {
      setResult(null);
      setError(submitError.message || "Errore imprevisto");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-shell">
      <header className="hero">
        <p className="eyebrow">Design exploration · split dashboard</p>
        <h1>Regressioni lineari e polinomiali</h1>
        <p className="subtitle">
          Modifica la tabella dati, lancia il calcolo e confronta i modelli
          nello stesso grafico.
        </p>
      </header>

      <main className="workspace">
        <form className="panel dataset-panel" onSubmit={handleSubmit}>
          <div className="panel-head">
            <div>
              <p className="kicker">Dataset · {pointsCount} punti</p>
              <h2>Input</h2>
            </div>
            <div className="mode-switch">
              <button
                type="button"
                className={mode === "manual" ? "tiny active" : "tiny"}
                onClick={() => setMode("manual")}
              >
                Tabella
              </button>
              <button
                type="button"
                className={mode === "csv" ? "tiny active" : "tiny"}
                onClick={() => setMode("csv")}
              >
                CSV
              </button>
            </div>
          </div>

          {mode === "manual" ? (
            <>
              <div className="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>#</th>
                      <th>X</th>
                      <th>Y</th>
                      <th></th>
                    </tr>
                  </thead>
                  <tbody>
                    {points.map((point, index) => (
                      <tr key={`${index}-${point.x}-${point.y}`}>
                        <td>{index + 1}</td>
                        <td>
                          <input
                            value={point.x}
                            onChange={(event) =>
                              updatePoint(index, "x", event.target.value)
                            }
                            aria-label={`x-${index + 1}`}
                          />
                        </td>
                        <td>
                          <input
                            value={point.y}
                            onChange={(event) =>
                              updatePoint(index, "y", event.target.value)
                            }
                            aria-label={`y-${index + 1}`}
                          />
                        </td>
                        <td>
                          <button
                            type="button"
                            className="icon"
                            onClick={() => removeRow(index)}
                          >
                            ×
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              <div className="inline-actions">
                <button type="button" className="tiny" onClick={addRow}>
                  + Riga
                </button>
                <button
                  type="button"
                  className="tiny"
                  onClick={() => setPoints(INITIAL_POINTS)}
                >
                  Dataset curvo
                </button>
                <button
                  type="button"
                  className="tiny"
                  onClick={() => setPoints(LINEAR_SAMPLE)}
                >
                  Dataset lineare
                </button>
              </div>
            </>
          ) : (
            <div className="csv-area">
              <label htmlFor="csv-input">Carica file CSV (colonne x,y)</label>
              <input
                id="csv-input"
                type="file"
                accept=".csv,text/csv"
                onChange={(event) =>
                  setCsvFile(event.target.files?.[0] || null)
                }
              />
            </div>
          )}

          <div className="controls-row">
            <label htmlFor="degree">Grado</label>
            <input
              id="degree"
              type="number"
              min="1"
              value={degree}
              onChange={(event) => setDegree(event.target.value)}
            />
          </div>

          <button className="primary" type="submit" disabled={loading}>
            {loading ? "Calcolo in corso..." : "Calcola regressione"}
          </button>

          {error ? <p className="error">{error}</p> : null}
        </form>

        <section className="panel chart-panel">
          <div className="panel-head">
            <div>
              <p className="kicker">Regressione</p>
              <h2>Confronto modelli</h2>
            </div>
            <p className="meta">
              {result
                ? `${result.points_count} osservazioni`
                : "In attesa dati"}
            </p>
          </div>

          <div className="chart-stage">
            {chartData ? (
              <Scatter data={chartData} options={chartOptions} />
            ) : (
              <p className="empty">Nessun grafico disponibile.</p>
            )}
          </div>

          <div className="models-grid">
            <article className="model-card linear">
              <h3>Lineare</h3>
              <p className="equation">
                {result?.linear.equation ?? "y = mx + q"}
              </p>
              <p>R²: {result?.linear.r_squared?.toFixed(6) ?? "n/a"}</p>
            </article>
            <article className="model-card poly">
              <h3>Polinomiale · grado {result?.polynomial.degree ?? degree}</h3>
              <p className="equation">
                {result?.polynomial.equation ?? "y = ax^n + ..."}
              </p>
              <p>R²: {result?.polynomial.r_squared?.toFixed(6) ?? "n/a"}</p>
            </article>
          </div>
        </section>
      </main>
    </div>
  );
}
