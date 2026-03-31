@echo off
setlocal
REM Entra na pasta onde este .bat está salvo
cd /d "%~dp0"

REM Prefere a venv local; se não existir, tenta py e depois python
set "PYTHON_CMD=%~dp0.venv\Scripts\python.exe"
if exist "%PYTHON_CMD%" goto run

where py >nul 2>nul
if %errorlevel%==0 (
    set "PYTHON_CMD=py -3"
    goto run
)

where python >nul 2>nul
if %errorlevel%==0 (
    set "PYTHON_CMD=python"
    goto run
)

echo Python nao encontrado.
echo Crie uma venv com: python -m venv .venv
echo Depois instale as dependencias com: .venv\Scripts\python -m pip install -r requirements.txt
pause
exit /b 1

:run
REM Abre um novo processo de console rodando o Streamlit e libera este .bat
start "CalendarioEscritorio" cmd /k %PYTHON_CMD% -m streamlit run controle_escritorio.py --server.port 8501

exit
