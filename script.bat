@echo off

:: put your api_key you want to use here 
set API_KEY_SCRIPT=key
set FLASK_ENV_SCRIPT=PRODUCTION

cd /d %~dp0
python server.py
