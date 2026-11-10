<#
.SYNOPSIS
    PasarSemaka Launcher - PowerShell Edition
    Pasar Digital Produk Lokal Kabupaten Tanggamus (Smart Economy)
    Copyright (c) 2026 by Athi Cahyani R dan Dr. Erliyan Redy Susanto, M.Kom.
#>

$Host.UI.RawUI.WindowTitle = "PasarSemaka Server Launcher"

Write-Host "======================================================================" -ForegroundColor DarkGreen
Write-Host "   PASARSEMAKA - PASAR DIGITAL PRODUK LOKAL KABUPATEN TANGGAMUS" -ForegroundColor Yellow
Write-Host "   Inisiatif Smart Economy Pemkab Tanggamus & Univ. Teknokrat Indonesia" -ForegroundColor Cyan
Write-Host "   Copyright (c) 2026 by Athi Cahyani R dan Dr. Erliyan Redy Susanto, M.Kom." -ForegroundColor Gray
Write-Host "======================================================================" -ForegroundColor DarkGreen
Write-Host ""

# 1. Cari Python executable
$pythonPaths = @(
    "C:\Users\user\AppData\Local\Programs\Orange\python.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python310\python.exe"
)

$pythonExe = $null

foreach ($p in $pythonPaths) {
    if (Test-Path $p) {
        $pythonExe = $p
        break
    }
}

if (-not $pythonExe) {
    $cmd = Get-Command python -ErrorAction SilentlyContinue
    if ($cmd) { $pythonExe = $cmd.Source }
}

if (-not $pythonExe) {
    Write-Host "[ERROR] Python 3.8+ tidak ditemukan di sistem." -ForegroundColor Red
    Read-Host "Tekan Enter untuk keluar"
    exit 1
}

Write-Host "[OK] Menggunakan runtime: $pythonExe" -ForegroundColor Green
Write-Host "[INFO] Memulai server PasarSemaka di http://localhost:8080 ..." -ForegroundColor Cyan

# Buka browser otomatis
Start-Job -ScriptBlock {
    Start-Sleep -Seconds 2
    Start-Process "http://localhost:8080"
} | Out-Null

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# Jalankan server
& $pythonExe "$scriptDir\server.py" 8080

