import subprocess
import sys

def check_git_repo():
    """Vérifie qu'on est bien dans un repo git."""
    result = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print("❌ Tu n'es pas dans un repo git.")
        sys.exit(1)

def get_staged_diff():
    """Récupère le diff des fichiers stagés."""
    result = subprocess.run(
        ["git", "diff", "--cached"],
        capture_output=True, text=True
    )
    diff = result.stdout.strip()
    if not diff:
        print("❌ Aucun fichier stagé. Fais d'abord un `git add`.")
        sys.exit(1)
    return diff

def get_staged_files():
    """Retourne la liste des fichiers stagés."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        capture_output=True, text=True
    )
    return result.stdout.strip().splitlines()

def do_commit(message):
    """Exécute le commit avec le message donné."""
    result = subprocess.run(
        ["git", "commit", "-m", message],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"✅ Commit effectué :\n   {message}")
    else:
        print(f"❌ Erreur lors du commit :\n{result.stderr}")
        sys.exit(1)