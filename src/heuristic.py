import os
from typing import List

# Règles : si un fichier matche → on suggère ce type
RULES = [
    (["test_", "_test.", ".spec.", ".test."], "test"),
    (["package.json", "requirements.txt", "pyproject.toml",
      "Makefile", "Dockerfile", ".github/", ".gitignore",
      "setup.cfg", "setup.py"], "chore"),
    (["README", ".md", "docs/", "CHANGELOG"], "docs"),
    (["fix", "bug", "hotfix", "patch"], "fix"),
    (["refactor", "clean", "rename", "move"], "refactor"),
]

def detect_type(staged_files: List[str]) -> str:
    """
    Analyse les noms de fichiers stagés et devine le type Conventional Commit.
    Retourne 'feat' par défaut si rien ne matche.
    """
    for file in staged_files:
        filename = os.path.basename(file).lower()
        filepath = file.lower()
        for patterns, commit_type in RULES:
            for pattern in patterns:
                if pattern.lower() in filename or pattern.lower() in filepath:
                    return commit_type
    return "feat"  # fallback par défaut