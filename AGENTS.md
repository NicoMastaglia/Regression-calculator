# Regression Project

Mini guida operativa per sviluppatori e coding agent.

## Scope

- Stack: FastAPI backend + React/Vite frontend.
- Obiettivo: regressione lineare e polinomiale da punti o CSV.

## Struttura

- `backend/`: API FastAPI (entrypoint `backend/main.py`).
- `frontend/`: app React/Vite (entrypoint `frontend/src/main.jsx`).
- `start.bat`: avvio backend + frontend da root (Windows).

## Avvio rapido

```bat
start.bat
```

URL attesi:

- Backend: `http://127.0.0.1:8000`
- Frontend: `http://127.0.0.1:5173` (se occupata: 5174, 5175, ...)

Avvio manuale:

```bat
cd /d backend
python main.py

cd /d ..\frontend
npm run dev -- --host 127.0.0.1
```

## API backend

- `GET /`: health (`{"message":"Regression API is running"}`).
- `POST /regression/points`: body JSON con `x`, `y`, `degree`.
- `POST /regression/csv?degree=2`: body CSV binario (`application/octet-stream`).

Regole utili:

- Eseguire backend da cartella `backend/`.
- Import backend via `src.linear_regression`.
- Errori di validazione/dominio: HTTP 400.

## Comandi sviluppo

```bat
cd /d backend
python main.py
python -m src.linear_regression

cd /d ..\frontend
npm run dev
npm run build
npm run preview
```

## Smoke test minimi

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/" | ConvertTo-Json -Compress

$body = @{ x=@(1,2,3,4); y=@(2,4,5,8); degree=2 } | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:8000/regression/points" -Method Post -ContentType "application/json" -Body $body

$csv = "x,y`n1,2`n2,4`n3,6"
$bytes = [System.Text.Encoding]::UTF8.GetBytes($csv)
Invoke-RestMethod -Uri "http://127.0.0.1:8000/regression/csv?degree=2" -Method Post -ContentType "application/octet-stream" -Body $bytes
```

```bat
cd /d frontend
npm run build
```

## Regole agent

- Non cambiare API pubbliche senza allineare frontend e docs.
- Preferire fix minimi, evitare refactor non richiesti.
- Dopo modifiche backend: testare almeno `GET /` e `POST /regression/points`.
- Dopo modifiche frontend: eseguire almeno `npm run build`.
- Per richieste production-ready, usare la skill `.github/skills/production-code-guard/SKILL.md`.

## Limiti correnti

- Nessuna suite test automatica.
- Nessun linter/formattatore formalizzato.
- Script di startup orientato a Windows.
