@echo off
chcp 65001 >nul
title Email Auto-Registrator v3

echo ================================================
echo   Проверка зависимостей...
echo ================================================
echo.

pip --version >nul 2>&1
if errorlevel 1 (
    echo ОШИБКА: pip не найден!
    echo Установи Python с https://python.org
    pause
    exit
)

echo Установка/обновление библиотек...
pip install -r requirements.txt --quiet --disable-pip-version-check

if errorlevel 1 (
    echo.
    echo ОШИБКА установки зависимостей!
    echo Попробуй вручную: pip install -r requirements.txt
    pause
    exit
)

echo.
echo ================================================
echo   Запуск программы...
echo ================================================
echo.

python email_registrator.py

if errorlevel 1 (
    echo.
    echo ================================================
    echo ОШИБКА запуска скрипта!
    echo ================================================
    pause
)