@echo off
REM Caminho da pasta do projeto
cd /d C:\Users\aloysio.filho\repos\calendario

REM Abre um novo processo de console rodando o Streamlit e libera este .bat
start "CalendarioEscritorio" cmd /c ^
"C:\Python314\python.exe" -m streamlit run controle_escritorio.py --server.port 8501

exit
