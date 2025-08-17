# Script PowerShell pour construire l'exécutable YouTube to TikTok
# Exécutez ce script en tant qu'administrateur si nécessaire

param(
    [switch]$Clean,
    [switch]$Installer,
    [switch]$NoIcon,
    [switch]$Help
)

if ($Help) {
    Write-Host "Usage: .\build_exe.ps1 [-Clean] [-Installer] [-NoIcon] [-Help]" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Options:" -ForegroundColor Yellow
    Write-Host "  -Clean      : Nettoie les anciens builds avant construction" -ForegroundColor White
    Write-Host "  -Installer  : Crée aussi le script d'installateur Inno Setup" -ForegroundColor White
    Write-Host "  -NoIcon     : Ne crée pas d'icône automatiquement" -ForegroundColor White
    Write-Host "  -Help       : Affiche cette aide" -ForegroundColor White
    exit 0
}

# Configuration de l'encodage pour les caractères français
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "========================================" -ForegroundColor Green
Write-Host "Construction de l'exécutable YouTube to TikTok" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Vérifier que Python est installé
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Python non trouvé"
    }
    Write-Host "✓ Python trouvé" -ForegroundColor Green
    Write-Host $pythonVersion -ForegroundColor White
} catch {
    Write-Host "❌ ERREUR: Python n'est pas installé ou n'est pas dans le PATH" -ForegroundColor Red
    Write-Host "Veuillez installer Python 3.8+ depuis https://python.org" -ForegroundColor Yellow
    Read-Host "Appuyez sur Entrée pour continuer"
    exit 1
}

# Construire les arguments pour le script Python
$args = @()

if ($Clean) {
    $args += "--clean"
}

if ($Installer) {
    $args += "--installer"
}

if ($NoIcon) {
    $args += "--no-icon"
}

Write-Host ""
Write-Host "🔨 Construction de l'exécutable..." -ForegroundColor Yellow

# Exécuter le script de construction Python
try {
    if ($args.Count -gt 0) {
        python build_exe.py @args
    } else {
        python build_exe.py
    }
    
    if ($LASTEXITCODE -ne 0) {
        throw "Échec de la construction"
    }
    
    Write-Host ""
    Write-Host "🎉 Construction terminée avec succès!" -ForegroundColor Green
    Write-Host ""
    
    # Vérifier que l'exécutable a été créé
    if (Test-Path "dist\YouTube-to-TikTok.exe") {
        $exeSize = (Get-Item "dist\YouTube-to-TikTok.exe").Length / 1MB
        Write-Host "✓ Exécutable créé: dist\YouTube-to-TikTok.exe" -ForegroundColor Green
        Write-Host "  Taille: $([math]::Round($exeSize, 1)) MB" -ForegroundColor White
        
        if ($Installer) {
            if (Test-Path "installer\YouTube-to-TikTok-Setup.exe") {
                Write-Host "✓ Installateur créé: installer\YouTube-to-TikTok-Setup.exe" -ForegroundColor Green
            } else {
                Write-Host "⚠ Installateur non trouvé (Inno Setup requis)" -ForegroundColor Yellow
            }
        }
        
        Write-Host ""
        Write-Host "L'application est prête à être distribuée!" -ForegroundColor Green
    } else {
        Write-Host "⚠ Exécutable non trouvé dans le dossier dist/" -ForegroundColor Yellow
    }
    
} catch {
    Write-Host ""
    Write-Host "❌ Échec de la construction: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Read-Host "Appuyez sur Entrée pour continuer"
