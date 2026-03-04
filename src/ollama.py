import requests
import sys

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral"
MAX_DIFF_CHARS = 4000  # ~1000 tokens, suffisant pour un diff normal

PROMPT_TEMPLATE = """You are a git commit message assistant.
Analyze the following git diff and write a commit message.

Rules:
- Use Conventional Commits format: type: short description
- Types allowed: feat, fix, chore, docs, refactor, test, style
- Title only, NO body, NO bullet points
- Maximum 72 characters total
- Always write in English
- Be specific and concise

Git diff:
{diff}

Respond with ONLY the commit message, nothing else."""

def check_ollama():
    """Vérifie qu'Ollama est accessible."""
    try:
        response = requests.get("http://localhost:11434", timeout=3)
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Ollama n'est pas détecté sur cette machine.")
        print("")
        print("   Installe-le :")
        print("   → Mac   : brew install ollama")
        print("   → Linux : curl -fsSL https://ollama.com/install.sh | sh")
        print("   → Win   : https://ollama.com/download")
        print("")
        print("   Puis lance :")
        print("   → ollama serve   (démarre le serveur)")
        print("   → ollama pull mistral   (télécharge le modèle)")
        sys.exit(1)

def truncate_diff(diff: str) -> str:
    """Tronque le diff si trop long, en gardant le début."""
    if len(diff) <= MAX_DIFF_CHARS:
        return diff
    truncated = diff[:MAX_DIFF_CHARS]
    return truncated + "\n\n[... diff tronqué pour respecter la fenêtre de contexte ...]"

def generate_message(diff: str, fallback_type: str) -> str:
    """Envoie le diff à Ollama et retourne le message généré."""
    check_ollama()
    diff = truncate_diff(diff)
    prompt = PROMPT_TEMPLATE.format(diff=diff)
    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL, "prompt": prompt, "stream": False},
            timeout=30
        )
        response.raise_for_status()
        message = response.json().get("response", "").strip()
        # Nettoyage : enlève les guillemets si l'IA en met
        message = message.strip('"').strip("'")
        # Vérifie que le message a un type Conventional Commit
        # Sinon on préfixe avec le fallback heuristique
        known_types = ["feat", "fix", "chore", "docs", "refactor", "test", "style"]
        has_type = any(message.startswith(f"{t}:") or
                      message.startswith(f"{t}(") for t in known_types)
        if not has_type:
            message = f"{fallback_type}: {message}"
        # Tronque si > 72 caractères
        if len(message) > 72:
            message = message[:72]
        return message
    except requests.exceptions.Timeout:
        print("⚠️  Ollama a mis trop de temps à répondre.")
        print(f"   Utilisation de l'heuristique : type détecté = '{fallback_type}'")
        return None
    except Exception as e:
        print(f"❌ Erreur Ollama : {e}")
        return None