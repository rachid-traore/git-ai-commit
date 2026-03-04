# git-ai-commit

> Generate smart commit messages using AI — powered by Ollama (local, private).

## Prerequisites

- Python 3.8+
- Ollama installed and running

## Install everything in one command
```bash
curl -fsSL https://raw.githubusercontent.com/rachid-traore/git-ai-commit/main/install.sh | sh
```

This script will automatically install Ollama, pull the `mistral` model, and install `git-ai-commit`.

## Manual installation

**1. Install Ollama**

| OS | Command |
|---|---|
| Mac | `brew install ollama` |
| Linux | `curl -fsSL https://ollama.com/install.sh \| sh` |
| Windows | [ollama.com/download](https://ollama.com/download) |

**2. Start Ollama and pull the model**
```bash
ollama serve &
ollama pull mistral
```

**3. Install git-ai-commit**
```bash
pip install git-ai-commit
```

## Usage
```bash
# Stage your changes
git add .

# Generate and commit
git ai-commit

# Open message in $EDITOR before committing
git ai-commit --edit
```

## Example output
```
🤖 Analyse du diff en cours...
→ feat: add user authentication via JWT

[Y] Valider  [e] Éditer  [n] Annuler :
```

## How it works

1. Reads your staged diff (`git diff --cached`)
2. Detects commit type instantly via heuristics (`feat`, `fix`, `chore`...)
3. Sends diff to local Ollama (`mistral` model)
4. Proposes a [Conventional Commits](https://www.conventionalcommits.org) message
5. You validate, edit, or cancel

## Privacy

Your code never leaves your machine. Ollama runs 100% locally.

## License

MIT