param(
    [string]$ServiceName = "CalendarioEscritorio",
    [string]$Port = "8501",
    [string]$NssmPath = "nssm.exe",
    [string]$RunAsUser = "",
    [string]$RunAsPassword = "",
    [switch]$UseCurrentUser
)

$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonExe = Join-Path $projectRoot ".venv\Scripts\python.exe"
$stdoutLog = Join-Path $projectRoot "logs\streamlit-service-out.log"
$stderrLog = Join-Path $projectRoot "logs\streamlit-service-err.log"
$logsDir = Split-Path -Parent $stdoutLog

if (-not (Test-Path $NssmPath)) {
    $resolvedNssm = Get-Command $NssmPath -ErrorAction SilentlyContinue
    if ($resolvedNssm) {
        $NssmPath = $resolvedNssm.Source
    } else {
        throw "NSSM nao encontrado. Informe -NssmPath com o caminho completo para nssm.exe."
    }
}

if (-not (Test-Path $pythonExe)) {
    throw "Python da venv nao encontrado em $pythonExe. Recrie a venv antes de instalar o servico."
}

New-Item -ItemType Directory -Force -Path $logsDir | Out-Null

$appParameters = "-m streamlit run controle_escritorio.py --server.headless true --server.port $Port --browser.gatherUsageStats false"

if ($UseCurrentUser -and -not $RunAsUser) {
    $RunAsUser = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
}

& sc.exe query $ServiceName *> $null
if ($LASTEXITCODE -eq 0) {
    & $NssmPath remove $ServiceName confirm | Out-Null
}

& $NssmPath install $ServiceName $pythonExe $appParameters
& $NssmPath set $ServiceName AppDirectory $projectRoot
& $NssmPath set $ServiceName DisplayName $ServiceName
& $NssmPath set $ServiceName Description "Calendario Streamlit executado em background via NSSM."
& $NssmPath set $ServiceName Start SERVICE_AUTO_START
& $NssmPath set $ServiceName AppStdout $stdoutLog
& $NssmPath set $ServiceName AppStderr $stderrLog
& $NssmPath set $ServiceName AppRotateFiles 1
& $NssmPath set $ServiceName AppRotateOnline 1
& $NssmPath set $ServiceName AppRotateSeconds 86400
& $NssmPath set $ServiceName AppExit Default Restart

if ($RunAsUser) {
    if (-not $RunAsPassword) {
        $securePassword = Read-Host "Digite a senha do usuario $RunAsUser" -AsSecureString
        $bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($securePassword)
        try {
            $RunAsPassword = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr)
        } finally {
            if ($bstr -ne [IntPtr]::Zero) {
                [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)
            }
        }
    }

    if (-not $RunAsPassword) {
        throw "Nao foi possivel obter a senha do usuario informado."
    }
    & $NssmPath set $ServiceName ObjectName $RunAsUser $RunAsPassword
}

Write-Host ""
Write-Host "Servico '$ServiceName' configurado com sucesso."
Write-Host "Para iniciar agora: nssm start $ServiceName"
Write-Host "URL esperada: http://localhost:$Port"

if (-not $RunAsUser) {
    Write-Host ""
    Write-Host "Importante: como o projeto esta em um perfil de usuario, prefira executar o servico com sua conta do Windows."
    Write-Host "Use -UseCurrentUser ou informe -RunAsUser DOMINIO\\usuario."
}
