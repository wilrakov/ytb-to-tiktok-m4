# Script PowerShell pour lancer l'interface graphique YouTube to TikTok
# Exécution : Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

param(
    [switch]$Test,
    [switch]$Help
)

function Show-Help {
    Write-Host "=== Lanceur Interface Graphique YouTube to TikTok ===" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  .\lancer_interface.ps1          # Lance l'interface graphique"
    Write-Host "  .\lancer_interface.ps1 -Test    # Lance les tests de vérification"
    Write-Host "  .\lancer_interface.ps1 -Help    # Affiche cette aide"
    Write-Host ""
    Write-Host "Options:" -ForegroundColor Yellow
    Write-Host "  -Test    Lance les tests de vérification avant le lancement"
    Write-Host "  -Help    Affiche cette aide"
    Write-Host ""
}

function Test-PythonInstallation {
    Write-Host "Vérification de l'installation Python..." -ForegroundColor Green
    
    try {
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Python installé: $pythonVersion" -ForegroundColor Green
            return $true
        }
    } catch {
        Write-Host "✗ Python non trouvé" -ForegroundColor Red
        return $false
    }
    
    Write-Host "✗ Python non trouvé ou non dans le PATH" -ForegroundColor Red
    Write-Host "Veuillez installer Python depuis https://python.org" -ForegroundColor Yellow
    return $false
}

function Test-Tkinter {
    Write-Host "Vérification de tkinter..." -ForegroundColor Green
    
    try {
        python -c "import tkinter; print('tkinter disponible')" 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ tkinter disponible" -ForegroundColor Green
            return $true
        }
    } catch {
        Write-Host "✗ tkinter non disponible" -ForegroundColor Red
        return $false
    }
    
    Write-Host "✗ tkinter non disponible" -ForegroundColor Red
    Write-Host "Veuillez réinstaller Python avec tkinter" -ForegroundColor Yellow
    return $false
}

function Test-Dependencies {
    Write-Host "Vérification des dépendances..." -ForegroundColor Green
    
    try {
        python -c "import yt_dlp, rich, PIL" 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Dépendances installées" -ForegroundColor Green
            return $true
        }
    } catch {
        Write-Host "✗ Dépendances manquantes" -ForegroundColor Red
        return $false
    }
    
    Write-Host "✗ Dépendances manquantes" -ForegroundColor Red
    Write-Host "Exécutez: pip install -r requirements.txt" -ForegroundColor Yellow
    return $false
}

function Launch-GUI {
    Write-Host "Lancement de l'interface graphique..." -ForegroundColor Green
    
    try {
        python launch_gui.py
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Interface fermée normalement" -ForegroundColor Green
        } else {
            Write-Host "Erreur lors de l'exécution (code: $LASTEXITCODE)" -ForegroundColor Red
        }
    } catch {
        Write-Host "Erreur lors du lancement: $_" -ForegroundColor Red
    }
}

function Run-Tests {
    Write-Host "Lancement des tests..." -ForegroundColor Green
    
    try {
        python test_gui.py
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Tous les tests sont passés" -ForegroundColor Green
            return $true
        } else {
            Write-Host "✗ Certains tests ont échoué" -ForegroundColor Red
            return $false
        }
    } catch {
        Write-Host "Erreur lors des tests: $_" -ForegroundColor Red
        return $false
    }
}

# Gestion des paramètres
if ($Help) {
    Show-Help
    exit 0
}

# Affichage du titre
Write-Host "=== YouTube to TikTok - Interface Graphique ===" -ForegroundColor Cyan
Write-Host ""

# Vérifications préliminaires
if (-not (Test-PythonInstallation)) {
    Read-Host "Appuyez sur Entrée pour fermer"
    exit 1
}

if (-not (Test-Tkinter)) {
    Read-Host "Appuyez sur Entrée pour fermer"
    exit 1
}

if (-not (Test-Dependencies)) {
    Write-Host ""
    Write-Host "Voulez-vous continuer quand même ? (y/N)" -ForegroundColor Yellow
    $response = Read-Host
    if ($response -notmatch "^[Yy]") {
        Read-Host "Appuyez sur Entrée pour fermer"
        exit 1
    }
}

# Lancement des tests si demandé
if ($Test) {
    Write-Host ""
    if (-not (Run-Tests)) {
        Write-Host ""
        Write-Host "Voulez-vous continuer quand même ? (y/N)" -ForegroundColor Yellow
        $response = Read-Host
        if ($response -notmatch "^[Yy]") {
            Read-Host "Appuyez sur Entrée pour fermer"
            exit 1
        }
    }
}

# Lancement de l'interface
Write-Host ""
Launch-GUI

# Pause finale
Write-Host ""
Read-Host "Appuyez sur Entrée pour fermer"
