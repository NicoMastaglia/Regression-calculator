# Regression Project

Applicazione full stack per calcolare e visualizzare regressione lineare e polinomiale a partire da punti inseriti manualmente o da file CSV.

## Panoramica

Il progetto e composto da:

- Backend FastAPI con endpoint REST per il calcolo delle regressioni.
- Frontend React + Vite con interfaccia grafica per input dati, confronto modelli e grafico.
- Modulo Python riusabile (`src.linear_regression`) con CLI dedicata.

## Funzionalita

- Regressione lineare ($y = mx + q$)
- Regressione polinomiale di grado configurabile
- Input da tabella (manuale) o upload CSV
- Visualizzazione grafica dei punti e delle curve di fit
- Risposta API con coefficienti, equazione e $R^2$

## Stack Tecnologico

- Backend: FastAPI, Pydantic, NumPy, Matplotlib, Uvicorn
- Frontend: React 18, Vite 5, Chart.js
- Ambiente target: Windows (comandi pronti anche per PowerShell)

## Struttura Progetto

```text
regression-project/
|- backend/
|  |- main.py
|  |- requirements.txt
|  |- dati.csv
|  \- src/linear_regression/
|- frontend/
|  |- package.json
|  \- src/
|- start.bat
\- AGENTS.md
```

## Prerequisiti

- Python 3.10+
- Node.js 18+ (consigliato 20+)
- npm

## Avvio Rapido (Windows)

Dalla root del progetto:

```bat
start.bat
```

Servizi attesi:

- Backend: http://127.0.0.1:8000
- Frontend: http://127.0.0.1:5173

Nota: se la porta frontend e occupata, Vite usa automaticamente 5174, 5175, ecc.

## Avvio Manuale

### 1) Backend

```bat
cd /d backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

In alternativa, senza virtualenv:

```bat
cd /d backend
py -3 -m pip install -r requirements.txt
py -3 main.py
```

### 2) Frontend

In un secondo terminale:

```bat
cd /d frontend
npm install
npm run dev -- --host 127.0.0.1
```

## Configurazione Frontend

Il frontend usa per default:

```text
http://127.0.0.1:8000
```

Puoi cambiarlo impostando la variabile ambiente `VITE_API_BASE_URL`.

## API Backend

### GET /

Health check.

Risposta:

```json
{ "message": "Regression API is running" }
```

### POST /regression/points

Calcola regressione lineare e polinomiale da array JSON.

Body:

```json
{
  "x": [1, 2, 3, 4],
  "y": [2, 4, 5, 8],
  "degree": 2
}
```

### POST /regression/csv?degree=2

Calcola regressione da CSV inviato come body binario (`application/octet-stream`).

Formato CSV atteso:

```csv
x,y
1,2
2,4
3,6
```

## Esempi PowerShell

### Health

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/" | ConvertTo-Json -Compress
```

### Regressione da punti

```powershell
$body = @{ x=@(1,2,3,4); y=@(2,4,5,8); degree=2 } | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:8000/regression/points" -Method Post -ContentType "application/json" -Body $body
```

### Regressione da CSV binario

```powershell
$csv = "x,y`n1,2`n2,4`n3,6"
$bytes = [System.Text.Encoding]::UTF8.GetBytes($csv)
Invoke-RestMethod -Uri "http://127.0.0.1:8000/regression/csv?degree=2" -Method Post -ContentType "application/octet-stream" -Body $bytes
```

## Uso del Modulo Python (CLI)

Da `backend/`:

```bat
python -m src.linear_regression
python -m src.linear_regression dati.csv
python -m src.linear_regression dati.csv --output output.png
```

## Build Frontend

```bat
cd /d frontend
npm run build
npm run preview
```

## Errori Comuni

- `ModuleNotFoundError` sul backend: avvia il backend da `backend/`.
- CORS/connessione frontend: verifica che backend sia su `127.0.0.1:8000` o aggiorna `VITE_API_BASE_URL`.
- Errore CSV: assicurati che il file sia UTF-8 e con almeno due colonne (`x`,`y`).

## Stato del Progetto

- Nessuna suite test automatica al momento.
- Nessun linter/formattatore formalizzato.

## Contribuire

Pull request benvenute. Per modifiche importanti, apri prima una issue con proposta tecnica.
