param(
    [string]$ServiceName = "CalendarioEscritorio",
    [string]$NssmPath = "nssm.exe"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $NssmPath)) {
    $resolvedNssm = Get-Command $NssmPath -ErrorAction SilentlyContinue
    if ($resolvedNssm) {
        $NssmPath = $resolvedNssm.Source
    } else {
        throw "NSSM nao encontrado. Informe -NssmPath com o caminho completo para nssm.exe."
    }
}

& $NssmPath stop $ServiceName 2>$null | Out-Null
& $NssmPath remove $ServiceName confirm

Write-Host "Servico '$ServiceName' removido."
