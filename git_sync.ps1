# ============================================================
# git_sync.ps1 — Sincronización UNIR → GitHub
# Ejecutar desde PowerShell en la carpeta UNIR
# ============================================================

$REPO_PATH = $PSScriptRoot
$GITHUB_USER = "pabdus"
$REPO_NAME = "UNIR"
$BRANCH = "main"

# --- Solicitar token si no está configurado ---
$remoteUrl = git -C $REPO_PATH remote get-url origin 2>$null
if (-not $remoteUrl) {
    $TOKEN = Read-Host "Ingresa tu GitHub Personal Access Token"
    git -C $REPO_PATH init
    git -C $REPO_PATH remote add origin "https://${GITHUB_USER}:${TOKEN}@github.com/${GITHUB_USER}/${REPO_NAME}.git"
    git -C $REPO_PATH branch -M $BRANCH
    Write-Host "✅ Repositorio remoto configurado." -ForegroundColor Green
}

# --- Actualizar README con fecha de hoy ---
$fecha = Get-Date -Format "yyyy-MM-dd"
$readmePath = Join-Path $REPO_PATH "README.md"
$content = Get-Content $readmePath -Raw

$newRow = "| $fecha | Sincronización automática quincenal | Archivos nuevos/modificados |"
if ($content -notmatch [regex]::Escape($fecha)) {
    $content = $content -replace "(\| 2026-.*\|.*\|.*\|)", "`$1`n$newRow"
    Set-Content $readmePath $content -NoNewline
    Write-Host "✅ README actualizado con fecha $fecha" -ForegroundColor Green
}

# --- Git add, commit, push ---
Set-Location $REPO_PATH
git add -A
$status = git status --porcelain
if ($status) {
    $commitMsg = "sync: actualizacion quincenal $fecha"
    git commit -m $commitMsg
    git push origin $BRANCH
    Write-Host "`n✅ Push exitoso a github.com/$GITHUB_USER/$REPO_NAME" -ForegroundColor Green
    Write-Host "Archivos subidos:" -ForegroundColor Cyan
    Write-Host $status
} else {
    Write-Host "ℹ️ No hay cambios nuevos para subir." -ForegroundColor Yellow
}
