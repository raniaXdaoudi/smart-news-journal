#!/bin/bash

# Script pour automatiser l'exécution quotidienne du projet
# Ce script doit être ajouté au crontab

# Chemins (à adapter selon votre installation)
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON_BIN="python3"
LOG_FILE="$PROJECT_DIR/logs/cron.log"

# Créer le dossier logs s'il n'existe pas
mkdir -p "$PROJECT_DIR/logs"

# Date et heure de début
echo "========================================" >> "$LOG_FILE"
echo "Début : $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"

# Se placer dans le répertoire du projet
cd "$PROJECT_DIR" || exit 1

# Exécuter le script
$PYTHON_BIN journal.py >> "$LOG_FILE" 2>&1

# Code de sortie
EXIT_CODE=$?
echo "Fin : $(date '+%Y-%m-%d %H:%M:%S') | Code: $EXIT_CODE" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

exit $EXIT_CODE

