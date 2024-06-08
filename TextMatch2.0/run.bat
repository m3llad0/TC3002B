@echo off

REM Navegar al directorio del backend y iniciar el servidor Flask
echo Iniciando servidor backend Flask...
cd backend
pip install -r requirements.txt
set FLASK_APP=app.py  REM Ajustar según el nombre de tu archivo principal de Flask si es diferente
start cmd /k flask run
set BACKEND_PID=%ERRORLEVEL%

REM Navegar al directorio del frontend y iniciar el servidor Next.js
echo Iniciando servidor frontend Next.js...
cd ../frontend
npm install
start npm run dev
set FRONTEND_PID=%ERRORLEVEL%

REM Función para matar los procesos cuando se termine el script
:cleanup
echo Deteniendo servidores...
taskkill /F /PID %BACKEND_PID%
taskkill /F /PID %FRONTEND_PID%
exit /B 0
