$ErrorActionPreference = 'Stop'
# Flutter and the Windows Java launcher need an ASCII path. Each checkout gets its own alias.
$projectRoot = [IO.Path]::GetFullPath((Split-Path $PSScriptRoot -Parent))
$pathBytes = [Text.Encoding]::UTF8.GetBytes($projectRoot.ToLowerInvariant())
$projectKey = [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($pathBytes)).Substring(0, 12)
$aliasParent = Join-Path $env:LOCALAPPDATA 'BatteryCopilotProjects'
$projectAlias = Join-Path $aliasParent $projectKey
New-Item -ItemType Directory -Force -Path $aliasParent | Out-Null
if (!(Test-Path -LiteralPath $projectAlias)) {
    New-Item -ItemType Junction -Path $projectAlias -Target $projectRoot | Out-Null
}
if ((Get-Item -LiteralPath $projectAlias).Target -ne $projectRoot) {
    throw 'Project alias points to a different checkout.'
}
$projectAlias
