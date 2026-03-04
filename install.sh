#!/bin/sh
set -e

echo "🚀 Installation de git-ai-commit..."

# 1. Vérifie Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 est requis."
    echo "   → https://www.python.org/downloads/"
    exit 1
fi

# 2. Installe Ollama si absent
if ! command -v ollama &> /dev/null; then
    echo "📦 Installation d'Ollama..."
    if [ "$(uname)" = "Darwin" ]; then
        brew install ollama
    elif [ "$(uname)" = "Linux" ]; then
        curl -fsSL https://ollama.com/install.sh | sh
    else
        echo "⚠️  Windows détecté : télécharge Ollama sur https://ollama.com/download"
        echo "   Puis relance ce script."
        exit 1
    fi
else
    echo "✅ Ollama déjà installé"
fi

# 3. Démarre Ollama en arrière-plan si pas lancé
if ! curl -s http://localhost:11434 > /dev/null 2>&1; then
    echo "▶️  Démarrage d'Ollama..."
    ollama serve &
    sleep 3
fi

# 4. Télécharge le modèle mistral si absent
if ! ollama list | grep -q "mistral"; then
    echo "📥 Téléchargement du modèle mistral (~4GB, une seule fois)..."
    ollama pull mistral
else
    echo "✅ Modèle mistral déjà présent"
fi

# 5. Installe le package Python
echo "📦 Installation de git-ai-commit..."
pip install git-ai-commit

echo ""
echo "✅ Installation terminée !"
echo "   Utilisation : git ai-commit"
echo "   Avec éditeur : git ai-commit --edit"