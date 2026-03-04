import os
import subprocess
import tempfile
import sys

def open_in_editor(message: str) -> str:
    """
    Ouvre le message dans $EDITOR pour que l'utilisateur puisse le modifier.
    Retourne le message modifié.
    """
    editor = os.environ.get("EDITOR", _default_editor())
    # Écrit le message dans un fichier temporaire
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False, prefix="git_ai_commit_"
    ) as f:
        f.write(message)
        f.write("\n\n# Modifie le message ci-dessus puis sauvegarde et ferme l'éditeur.")
        f.write("\n# Les lignes commençant par # sont ignorées.")
        tmp_path = f.name
    try:
        subprocess.call([editor, tmp_path])
        with open(tmp_path, "r") as f:
            lines = f.readlines()
        # Ignore les commentaires et lignes vides
        edited = "".join(
            line for line in lines
            if not line.startswith("#")
        ).strip()
        if not edited:
            print("❌ Message vide, commit annulé.")
            sys.exit(0)
        return edited
    finally:
        os.unlink(tmp_path)

def _default_editor():
    """Retourne un éditeur par défaut selon l'OS."""
    if os.name == "nt":  # Windows
        return "notepad"
    return "nano"        # Mac / Linux