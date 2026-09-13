$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
Set-Location $projectRoot
$env:PYTHONUTF8 = '1'
if (!(Get-Command uv -ErrorAction SilentlyContinue)) { throw 'Install uv first: https://docs.astral.sh/uv/getting-started/installation/' }
New-Item -ItemType Directory -Force '.runtime' | Out-Null
uv sync --python 3.11 --locked
if ($LASTEXITCODE -ne 0) { throw 'Python environment setup failed' }

$javaDirectory = Join-Path $env:LOCALAPPDATA 'BatteryCopilotJava21'
if (!(Test-Path $javaDirectory)) {
    $javaUrl = 'https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.12.1%2B1/OpenJDK21U-jre_x64_windows_hotspot_21.0.12.1_1.zip'
    Invoke-WebRequest $javaUrl -OutFile '.runtime/java21.zip'
    if ((Get-FileHash '.runtime/java21.zip' -Algorithm SHA256).Hash.ToLowerInvariant() -ne 'd35f31e712f0fcf6ac5a093edc90204fbff22f720ba3950bd09d331d5e621636') { throw 'Java download checksum mismatch' }
    Expand-Archive '.runtime/java21.zip' $javaDirectory
}
if (!(Test-Path '.runtime/neo4j-community-5.26.30')) {
    if (!(Test-Path '.runtime/neo4j.zip')) {
        Invoke-WebRequest 'https://dist.neo4j.org/neo4j-community-5.26.30-windows.zip' -OutFile '.runtime/neo4j.zip'
    }
    Expand-Archive '.runtime/neo4j.zip' '.runtime'
    Add-Content '.runtime/neo4j-community-5.26.30/conf/neo4j.conf' "`nserver.memory.heap.initial_size=256m`nserver.memory.heap.max_size=512m`nserver.memory.pagecache.size=256m`nserver.default_listen_address=127.0.0.1`ndbms.usage_report.enabled=false"
}
if (!(Test-Path '.runtime/flutter')) {
    git clone --depth 1 --branch 3.47.4 https://github.com/flutter/flutter.git .runtime/flutter
    if ($LASTEXITCODE -ne 0) { throw 'Flutter download failed' }
}
$projectAlias = & (Join-Path $PSScriptRoot 'project-path.ps1')
if (!(Test-Path 'data/sources/pem-module-pack-guide.pdf')) {
    Invoke-WebRequest 'https://vdma-branchenfuehrer.de/fileadmin/battprod/downloads/Production_modul_and_pack_assembly.pdf' -OutFile 'data/sources/pem-module-pack-guide.pdf'
}
Push-Location (Join-Path $projectAlias 'frontend')
try {
    & '../.runtime/flutter/bin/flutter.bat' pub get
    if ($LASTEXITCODE -ne 0) { throw 'Flutter dependency setup failed' }
    & '../.runtime/flutter/bin/flutter.bat' build web --no-web-resources-cdn
    if ($LASTEXITCODE -ne 0) { throw 'Flutter build failed' }
} finally { Pop-Location }
Write-Output 'Environment ready. Start Neo4j, then run the import commands in README.md.'
