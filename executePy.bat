@echo off
CD /D "E:\conda\condabin\"
call activate bpac
CD /D "E:\BestPriceAtCostcoProject"
python src\main.py
