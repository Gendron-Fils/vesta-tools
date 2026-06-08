# vesta-tools — Instructions du dépôt

## Ce que c'est

La boîte à outils Claude Code partagée de Gendron & Fils : un marketplace de plugins (`gendron-tools`) contenant le plugin `outils-gf`. On définit une commande une fois ici, les dépôts branchés la voient. Détails et structure dans le `README.md`.

## Règle d'or : dépôt PUBLIC

Ce dépôt est public pour que les sessions infonuagiques le clonent sans jeton. Donc :

- **Aucun secret.** Jamais de clé, de jeton, de mot de passe, même en exemple réaliste.
- **Aucun contenu propriétaire.** Pas de voix de marque détaillée codée en dur, pas de mémoire stratégique, pas de données client. Seulement des commandes génériques réutilisables.
- En cas de doute sur le caractère sensible d'un ajout, il ne va pas ici. Le cerveau `Gendron-Fils/vesta` (privé) est l'endroit pour le propriétaire.

## Conventions

- Noms verrouillés : marketplace `gendron-tools`, plugin `outils-gf`. Une commande s'invoque `/outils-gf:recap`.
- Une commande = un fichier `plugins/outils-gf/commands/<nom>.md`, frontmatter `description` et `argument-hint` optionnel.
- Voix : français québécois, pas de tiret cadratin dans la prose.
- Commits : conventional commits en français (`feat:`, `chore:`, `docs:`), trailer `Co-Authored-By: Claude <noreply@anthropic.com>`.
- Versionner le plugin : bumper `version` dans `plugins/outils-gf/.claude-plugin/plugin.json` quand on veut que les dépôts branchés reçoivent la mise à jour.
