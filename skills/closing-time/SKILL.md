---
name: closing-time
description: Routine de fin de session Gendron & Fils : mémoire, backlog, rétro, récap archivé. Invoquée par /closing-time.
---

# `/closing-time` — la clôture de conversation

**Ce skill est un POINTEUR, pas une copie.** La définition maîtresse vit dans le dépôt public
`Gendron-Fils/vesta-tools`, fichier `plugins/outils-gf/commands/closing-time.md`. Une règle a
une seule source : ne recopie jamais la routine ici, va la lire. Le skill n'existe que pour
porter la commande sur les surfaces où le plugin `outils-gf` n'est pas monté (mobile, sessions
infonuagiques), où elle rendait « Unknown command ».

## La routine

1. **Va chercher la définition maîtresse**, dans cet ordre :
   - le clone `vesta-tools` s'il est déjà dans la session : `plugins/outils-gf/commands/closing-time.md` ;
   - sinon, le dépôt est public et ne demande aucun jeton :
     `curl -sS https://raw.githubusercontent.com/Gendron-Fils/vesta-tools/main/plugins/outils-gf/commands/closing-time.md`
2. **Exécute-la telle qu'elle est écrite**, dans les conventions du dépôt courant (son
   `CLAUDE.md` et la mémoire qu'il référence), avec `$ARGUMENTS` comme sujet optionnel du récap.
3. **Si tu ne peux pas la lire** (pas de shell, pas de réseau) : dis-le franchement, puis fais
   la clôture selon les conventions du dépôt courant, sans inventer de geste que le dépôt n'a pas.

Ne réponds jamais « commande indisponible » : la définition est le contrat, le slash n'est que
le raccourci.
