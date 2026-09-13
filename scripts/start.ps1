$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
Set-Location $projectRoot
$env:PYTHONUTF8 = '1'
if (!(Get-NetTCPConnection -LocalPort 7687 -State Listen -ErrorAction SilentlyContinue)) {
    Start-Process -FilePath 'pwsh.exe' -WindowStyle Hidden -ArgumentList '-NoProfile','-File',('"' + (Join-Path $PSScriptRoot 'start-neo4j.ps1') + '"') -RedirectStandardOutput '.runtime/neo4j-stdout.log' -RedirectStandardError '.runtime/neo4j-stderr.log' | Out-Null
    for ($attempt = 0; $attempt -lt 45; $attempt++) {
        if (Get-NetTCPConnection -LocalPort 7687 -State Listen -ErrorAction SilentlyContinue) { break }
        Start-Sleep -Seconds 1
    }
}
uv run uvicorn battery_copilot.api:app --host 127.0.0.1 --port 8000
