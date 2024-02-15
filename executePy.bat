@echo off
CD /D "E:\conda\condabin\"
call activate bpac
CD /D "E:\BestPriceAtCostcoProject"
"E:\conda\envs\bpac\python.exe" "E:\BestPriceAtCostcoProject\src\main.py"