$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$runtimeAlias = Join-Path (& (Join-Path $PSScriptRoot 'project-path.ps1')) '.runtime'
# The Windows Java launcher requires an ASCII runtime path on this machine.
$neo4jRoot = Join-Path $runtimeAlias 'neo4j-community-5.26.30'
$env:JAVA_HOME = (Get-ChildItem (Join-Path $env:LOCALAPPDATA 'BatteryCopilotJava21') -Directory | Select-Object -First 1).FullName
$envPath = Join-Path $projectRoot '.env'
if (!(Test-Path $envPath)) {
    $localPassword = [guid]::NewGuid().ToString('N')
    (Get-Content (Join-Path $projectRoot '.env.example') -Raw).Replace('replace-with-local-password', $localPassword) | Set-Content $envPath -Encoding utf8
}
if (!(Test-Path (Join-Path $neo4jRoot 'data/dbms/auth.ini'))) {
    $localPassword = ((Get-Content $envPath | Where-Object { $_ -like 'NEO4J_PASSWORD=*' }) -split '=',2)[1]
    & (Join-Path $neo4jRoot 'bin/neo4j-admin.ps1') dbms set-initial-password $localPassword
    if ($LASTEXITCODE -ne 0) { throw 'Neo4j password initialization failed' }
}
& (Join-Path $neo4jRoot 'bin/neo4j.ps1') console
