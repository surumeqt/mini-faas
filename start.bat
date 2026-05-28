@echo off
title Starting Mini FaaS

:: Wait for the server to be up in the background, then launch index.html
start /b cmd /c "for /l %%i in (1,1,30) do (curl -s -o nul http://localhost:5000/ && start http://localhost:5000/index.html && exit) || (timeout /t 2 >nul)"

docker compose up --build

