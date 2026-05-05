<#
Script: push_repo.ps1
Uso: .\push_repo.ps1 -RepoName proyecto-ti
Este script inicializa git, hace commit y crea el repo en GitHub usando GH CLI si está disponible.
Si no tienes GH CLI, pasa la URL remota con -RemoteUrl.
#>

[CmdletBinding()]
param(
    [string]$RepoName = "proyecto-ti",
    [string]$RemoteUrl = ""
)

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error "Git no está instalado. Instala Git y vuelve a intentarlo."; exit 1
}

if (-not (Test-Path ".git")) {
    git init | Out-Null
    Write-Host "Repositorio git inicializado."
} else {
    Write-Host "Repositorio git ya inicializado."
}

git add .
git commit -m "Prepare app for Render deployment (Docker)" -q 2>$null || Write-Host "No hay cambios para commitear."

if (Get-Command gh -ErrorAction SilentlyContinue) {
    try {
        gh auth status -t > $null 2>&1
    } catch {
        Write-Host "Inicia sesión en GH CLI: gh auth login"; exit 1
    }

    if ($RemoteUrl -ne "") {
        git remote add origin $RemoteUrl 2>$null
        git branch -M main
        git push -u origin main
    } else {
        gh repo create $RepoName --public --source=. --remote=origin --push
    }
} else {
    if ($RemoteUrl -eq "") {
        Write-Host "GH CLI no encontrado. Crea el repo en GitHub manualmente y luego ejecuta:";
        Write-Host "  git remote add origin https://github.com/USER/REPO.git";
        Write-Host "  git branch -M main";
        Write-Host "  git push -u origin main";
        exit 1
    } else {
        git remote add origin $RemoteUrl 2>$null
        git branch -M main
        git push -u origin main
    }
}

Write-Host "Push completado. Ahora conecta el repo en Render (https://render.com)."
