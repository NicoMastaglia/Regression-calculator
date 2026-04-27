@echo off
setlocal

set "ROOT_DIR=%~dp0"
set "BACKEND_DIR=%ROOT_DIR%backend"
set "FRONTEND_DIR=%ROOT_DIR%frontend"
set "BACKEND_VENV_PY=%BACKEND_DIR%\venv\Scripts\python.exe"

if not exist "%BACKEND_DIR%\main.py" (
    echo [ERRORE] File backend non trovato: "%BACKEND_DIR%\main.py"
    exit /b 1
)

if not exist "%FRONTEND_DIR%\package.json" (
    echo [ERRORE] File frontend non trovato: "%FRONTEND_DIR%\package.json"
    exit /b 1
)

echo Avvio servizi...
echo.

if exist "%BACKEND_VENV_PY%" (
    start "Regression Backend" cmd /k "cd /d ""%BACKEND_DIR%"" & ""%BACKEND_VENV_PY%"" main.py"
) else (
    start "Regression Backend" cmd /k "cd /d ""%BACKEND_DIR%"" & py -3 main.py"
)

start "Regression Frontend" cmd /k "cd /d ""%FRONTEND_DIR%"" & npm run dev -- --host 127.0.0.1"

echo Backend:  http://127.0.0.1:8000
echo Frontend: http://127.0.0.1:5173
echo Nota: se la porta 5173 e' occupata, Vite usera' automaticamente 5174, 5175, ...
echo.
echo Sono state aperte due finestre terminale (backend e frontend).

endlocal
