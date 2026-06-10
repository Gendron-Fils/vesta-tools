#!/usr/bin/env bash
#
# sync-commands.sh — Recopie les commandes de la boîte à outils partagée
# (plugin outils-gf) vers le .claude/commands/ des dépôts branchés.
#
# Pourquoi : dans une session Claude Code infonuagique (conteneur neuf), seul un
# fichier committé dans le dépôt cloné charge de façon garantie. Le plugin reste
# la librairie canonique (on définit un outil une fois ici) ; ce script propage le
# filet committé qui garantit /recap (et les futurs outils) dans le nuage.
#
# La mémoire « vesta » est VOLONTAIREMENT EXCLUE : elle reste pointeur seulement,
# jamais d'outillage committé dedans.
#
# Usage :
#   scripts/sync-commands.sh            # recopie vers tous les dépôts trouvés
#   scripts/sync-commands.sh --dry-run  # montre ce qui changerait, sans rien écrire
#   BASE_DIR=/un/chemin scripts/sync-commands.sh   # force le dossier parent des dépôts
#
# Marche en local comme dans le nuage : par défaut, les dépôts sont cherchés à côté
# de vesta-tools (même dossier parent). Additif et idempotent : il ajoute et met à
# jour, il ne supprime jamais. Retirer un outil d'un dépôt reste un geste manuel.
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$SCRIPT_DIR/../plugins/outils-gf/commands"

# Dossier parent des dépôts (par défaut : le parent de vesta-tools).
BASE_DIR="${BASE_DIR:-$(cd "$SCRIPT_DIR/../.." && pwd)}"

# Dépôts branchés qui reçoivent le filet de commandes. La mémoire « vesta » est exclue.
REPOS=(vesta-app coup-doeil seo-audit seo-audit-app website website-designer)

DRY_RUN=0
if [ "${1:-}" = "--dry-run" ] || [ "${1:-}" = "-n" ]; then
  DRY_RUN=1
fi

if [ ! -d "$SRC" ]; then
  echo "Erreur : dossier des commandes introuvable ($SRC). Lance le script depuis le dépôt vesta-tools." >&2
  exit 1
fi

shopt -s nullglob
SRC_FILES=("$SRC"/*.md)
if [ ${#SRC_FILES[@]} -eq 0 ]; then
  echo "Aucune commande à synchroniser dans $SRC." >&2
  exit 0
fi

echo "Source   : $SRC"
echo "Dépôts   : sous $BASE_DIR"
[ $DRY_RUN -eq 1 ] && echo "Mode     : aperçu (--dry-run), aucune écriture"
echo "Commandes: $(for f in "${SRC_FILES[@]}"; do basename "$f"; done | paste -sd' ' -)"
echo

changed_repos=()
missing_repos=()

for repo in "${REPOS[@]}"; do
  dest_repo="$BASE_DIR/$repo"
  if [ ! -d "$dest_repo" ]; then
    missing_repos+=("$repo")
    continue
  fi
  dest="$dest_repo/.claude/commands"
  repo_changed=0
  for src in "${SRC_FILES[@]}"; do
    name="$(basename "$src")"
    target="$dest/$name"
    if [ -f "$target" ] && cmp -s "$src" "$target"; then
      status="inchangé"
    elif [ -f "$target" ]; then
      status="mis à jour"
      repo_changed=1
    else
      status="ajouté"
      repo_changed=1
    fi
    if [ "$status" != "inchangé" ] && [ $DRY_RUN -eq 0 ]; then
      mkdir -p "$dest"
      cp "$src" "$target"
    fi
    echo "  [$repo] $name : $status"
  done
  [ $repo_changed -eq 1 ] && changed_repos+=("$repo")
done

echo
if [ ${#missing_repos[@]} -gt 0 ]; then
  echo "Dépôts non trouvés (ignorés) : ${missing_repos[*]}"
fi
if [ ${#changed_repos[@]} -eq 0 ]; then
  echo "Rien à changer : tous les dépôts sont déjà à jour."
else
  echo "Dépôts modifiés : ${changed_repos[*]}"
  if [ $DRY_RUN -eq 1 ]; then
    echo "Aperçu seulement. Relance sans --dry-run pour écrire."
  else
    echo "Prochaine étape : dans chaque dépôt modifié, committer le .claude/commands/ et ouvrir une PR vers main."
  fi
fi
