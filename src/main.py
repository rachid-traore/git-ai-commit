import sys
import argparse
from src.git import check_git_repo, get_staged_diff, get_staged_files, do_commit
from src.heuristic import detect_type
from src.ollama import generate_message
from src.editor import open_in_editor

def main():
    parser = argparse.ArgumentParser(
        description="🤖 Génère un message de commit via Ollama"
    )
    parser.add_argument(
        "--edit", "-e",
        action="store_true",
        help="Ouvre le message dans $EDITOR avant de committer"
    )
    args = parser.parse_args()

    # 1. Vérifications de base
    check_git_repo()

    # 2. Récupère les infos git
    diff = get_staged_diff()
    staged_files = get_staged_files()

    # 3. Heuristique immédiate (pendant qu'Ollama réfléchit)
    fallback_type = detect_type(staged_files)

    # 4. Génère le message via Ollama
    print("🤖 Analyse du diff en cours...")
    message = generate_message(diff, fallback_type)

    # 5. Si Ollama a échoué → on construit un message minimal avec l'heuristique
    if not message:
        staged_names = ", ".join(staged_files[:3])
        message = f"{fallback_type}: update {staged_names}"
        print(f"   Message de fallback : {message}")

    # 6. Mode --edit : ouvre dans $EDITOR
    if args.edit:
        message = open_in_editor(message)

    # 7. Affiche la proposition
    print(f"\n→ {message}\n")

    # 8. Demande confirmation
    try:
        choice = input("[Y] Valider  [e] Éditer  [n] Annuler : ").strip().lower()
    except KeyboardInterrupt:
        print("\n❌ Annulé.")
        sys.exit(0)

    if choice in ("", "y"):
        do_commit(message)
    elif choice == "e":
        message = open_in_editor(message)
        print(f"\n→ {message}\n")
        confirm = input("Valider ce message ? [Y/n] : ").strip().lower()
        if confirm in ("", "y"):
            do_commit(message)
        else:
            print("❌ Commit annulé.")
    else:
        print("❌ Commit annulé.")