---
name: mission
description: Rédige et dispatche un ordre de mission pour un agent Claude Code, ou en exécute un existant. Invoquée par /mission.
---

# `/mission` — l'ordre de mission

**Ce skill est un POINTEUR, pas une copie.** La définition maîtresse vit dans le dépôt public
`Gendron-Fils/vesta-tools`, fichier `plugins/outils-gf/commands/mission.md`. Une règle a une
seule source : ne recopie jamais la routine ici, va la lire. C'est la leçon payée par ce
skill-ci : sa version copiée du 2026-05-29 a dérivé de la commande maîtresse pendant plus de
trois mois (13 653 octets contre 7 913 après le dégraissage de la 0.12.0), sans que rien ne le
signale. Un skill qui recopie une routine est une dérive en attente.

## La routine

1. **Va chercher la définition maîtresse**, dans cet ordre :
   - le clone `vesta-tools` s'il est déjà dans la session : `plugins/outils-gf/commands/mission.md` ;
   - sinon, le dépôt est public et ne demande aucun jeton :
     `curl -sS https://raw.githubusercontent.com/Gendron-Fils/vesta-tools/main/plugins/outils-gf/commands/mission.md`
2. **Exécute-la telle qu'elle est écrite**, avec ce que Philippe a écrit comme `$ARGUMENTS`.
   C'est elle qui décide du mode : un chemin vers un ordre existant veut dire l'exécuter,
   n'importe quoi d'autre veut dire le rédiger et le dispatcher.
3. **Si tu ne peux pas la lire** (pas de shell, pas de réseau) : dis-le franchement en une ligne
   plutôt que de rédiger un ordre de mission de mémoire. Un ordre de mission bâti sur un état
   inventé coûte plus cher que pas d'ordre du tout.

Ne réponds jamais « commande indisponible » : la définition est le contrat, le slash n'est que
le raccourci.
