@echo off
echo ==========================================
echo   ServiApp - Iniciando aplicacion...
echo ==========================================

REM Backend Django
start cmd /k "title Backend-Django && cd /d %~dp0 && .venv\Scripts\activate && python manage.py runserver"

REM Frontend Vue
start cmd /k "title Frontend-Vue && cd /d %~dp0frontend_vue && npm run dev"

timeout /t 3 /nobreak > nul

echo.
echo  Backend  ->  http://localhost:8000
echo  Frontend ->  http://localhost:5173
echo  Admin    ->  http://localhost:8000/admin
echo.
echo Abre http://localhost:5173 en tu navegador
pause
