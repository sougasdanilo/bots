$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

$python = Join-Path $projectRoot "venv\Scripts\python.exe"

if (-not (Test-Path $python)) {
    throw "Ambiente virtual nao encontrado em 'venv'. Crie-o com: python -m venv venv"
}

Write-Host "Instalando dependencias do projeto..."
& $python -m pip install -r requirements.txt

Write-Host "Instalando PyInstaller..."
& $python -m pip install pyinstaller

Write-Host "Gerando executavel..."

try {
    & $python -m PyInstaller --clean atalho_data.spec
} catch {
    $message = $_.Exception.Message

    if ($message -like "*dist\\atalho_data.exe*") {
        throw "Nao foi possivel sobrescrever dist\\atalho_data.exe. Feche o executavel aberto e rode o build novamente."
    }

    throw
}

Write-Host ""
Write-Host "Build concluida com sucesso em dist\\atalho_data.exe"
