<#
Script: run_local_docker.ps1
Uso: .\run_local_docker.ps1 -DatabaseUrl <url> -SupabaseUrl <url> -SupabaseKey <key>
Construye la imagen Docker y la ejecuta con las variables de entorno proporcionadas.
#>

param(
    [string]$DatabaseUrl = "",
    [string]$SupabaseUrl = "",
    [string]$SupabaseKey = ""
)

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Error "Docker no está instalado. Instala Docker Desktop y vuelve a intentarlo."; exit 1
}

if ($DatabaseUrl -eq "" -or $SupabaseUrl -eq "" -or $SupabaseKey -eq "") {
    Write-Host "Faltan variables. Puedes exportarlas antes o pasarlas como parámetros.";
    Write-Host "Ejemplo: .\run_local_docker.ps1 -DatabaseUrl 'postgresql://user:pass@host:5432/db' -SupabaseUrl 'https://...' -SupabaseKey 'key'"
    exit 1
}

docker build -t proyecto-ti .

docker run -e DATABASE_URL="$DatabaseUrl" -e SUPABASE_URL="$SupabaseUrl" -e SUPABASE_KEY="$SupabaseKey" -p 8000:8000 proyecto-ti
