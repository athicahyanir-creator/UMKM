@echo off
setlocal enabledelayedexpansion
title PasarSemaka - Smart City Kabupaten Tanggamus

echo ======================================================================
echo   PASARSEMAKA - PASAR DIGITAL PRODUK LOKAL KABUPATEN TANGGAMUS
echo   Inisiatif Smart Economy Pemkab Tanggamus ^& Univ. Teknokrat Indonesia
echo   Copyright (c) 2026 by Athi Cahyani R dan Dr. Erliyan Redy Susanto, M.Kom.
echo ======================================================================
echo.

rem 1. Deteksi executable Python
set PYTHON_CMD=

rem Cek instalasi spesifik di Orange
if exist "C:\Users\user\AppData\Local\Programs\Orange\python.exe" (
    set PYTHON_CMD="C:\Users\user\AppData\Local\Programs\Orange\python.exe"
    goto found_python
)

rem Cek python di PATH
python --version >nul 2>&1
if !errorlevel! equ 0 (
    set PYTHON_CMD=python
    goto found_python
)

rem Cek py launcher
py -0 >nul 2>&1
if !errorlevel! equ 0 (
    set PYTHON_CMD=py
    goto found_python
)

rem Cek instalasi standar LocalAppData
for /d %%i in ("%LOCALAPPDATA%\Programs\Python\Python*") do (
    if exist "%%i\python.exe" (
        set PYTHON_CMD="%%i\python.exe"
        goto found_python
    )
)

:found_python
if "%PYTHON_CMD%"=="" (
    echo [ERROR] Runtime Python 3.8+ tidak ditemukan.
    echo Harap instal Python dari https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Menggunakan runtime: %PYTHON_CMD%
echo [INFO] Menyiapkan basis data dan memulai server PasarSemaka...
echo [INFO] Membuka browser pada http://localhost:8080 ...
echo.

rem Buka browser otomatis setelah 1.5 detik di background
start "" /b cmd /c "timeout /t 2 /nobreak >nul && start http://localhost:8080"

rem Jalankan backend server
%PYTHON_CMD% "%~dp0server.py" 8080

pause

