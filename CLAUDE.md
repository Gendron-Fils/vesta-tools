# vesta-tools — Instructions du dépôt

## Ce que c'est

La boîte à outils Claude Code partagée de Gendron & Fils : un marketplace de plugins (`gendron-tools`) contenant le plugin `outils-gf`. On définit une commande une fois ici, les dépôts branchés la voient. Détails et structure dans le `README.md`.

## Règle d'or : dépôt PUBLIC

Ce dépôt est public pour que les sessions infonuagiques le clonent sans jeton. Donc :

- **Aucun secret.** Jamais de clé, de jeton, de mot de passe, même en exemple réaliste.
- **Aucun contenu propriétaire.** Pas de voix de marque détaillée codée en dur, pas de mémoire stratégique, pas de données client. Seulement des commandes génériques réutilisables.
- En cas de doute sur le caractère sensible d'un ajout, il ne va pas ici. La mémoire `Gendron-Fils/vesta` (privée) est l'endroit pour le propriétaire.

## Conventions

- Noms verrouillés : marketplace `gendron-tools`, plugin `outils-gf`. Une commande s'invoque `/outils-gf:recap`.
- Une commande = un fichier `plugins/outils-gf/commands/<nom>.md`, frontmatter `description` et `argument-hint` optionnel.
- Voix : français québécois, pas de tiret cadratin dans la prose.
- Commits : conventional commits en français (`feat:`, `chore:`, `docs:`), trailer `Co-Authored-By: Claude <noreply@anthropic.com>`.
- Versionner le plugin : bumper `version` dans `plugins/outils-gf/.claude-plugin/plugin.json` quand on veut que les dépôts branchés reçoivent la mise à jour. **Un bump n'est fini que propagé** : rouler `scripts/sync-commands.sh` et merger les PR de sync dans la foulée, sinon les copies vendorisées divergent en silence (dérive attrapée le 2026-07-17 : maîtres à 0.11.0, copies à 0.9.0 pendant 4 jours).

## Disponibilité des commandes dans le nuage

Le menu `/` et le plugin sont peu fiables en session Claude Code infonuagique : le menu ne lit que la racine de session et ses dossiers parents, jamais les sous-dossiers, et le plugin se charge tard ou pas du tout. Le canal fiable, c'est le fichier d'instructions (`CLAUDE.md`), toujours lu au démarrage.

Donc : les commandes de la boîte (`/recap`, `/closing-time`, `/mission`) sont définies dans ce dépôt, sous `plugins/outils-gf/commands/<nom>.md`. Si une de ces commandes est invoquée sans apparaître comme commande chargée, lire le fichier de définition correspondant et exécuter la routine telle qu'écrite, selon les conventions du dépôt courant. Ne jamais répondre « commande indisponible » : la définition est le contrat, le slash n'est que le raccourci.
