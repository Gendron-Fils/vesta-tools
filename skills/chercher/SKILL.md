---
name: chercher
description: Repêche un sujet dans la mémoire évolutive de Gendron & Fils (index plein-texte de Vesta). Invoquée par /chercher.
---

# `/chercher` — le repêchage dans la mémoire

**Ce skill est un POINTEUR, pas une copie.** La définition maîtresse vit dans le dépôt public
`Gendron-Fils/vesta-tools`, fichier `plugins/outils-gf/commands/chercher.md`. Une règle a une
seule source : ne recopie jamais la routine ici, va la lire. Le skill n'existe que pour porter
la commande sur les surfaces où le plugin `outils-gf` n'est pas monté (mobile, sessions
infonuagiques), où elle rendait « Unknown command ».

## La routine

1. **Va chercher la définition maîtresse**, dans cet ordre :
   - le clone `vesta-tools` s'il est déjà dans la session : `plugins/outils-gf/commands/chercher.md` ;
   - sinon, le dépôt est public et ne demande aucun jeton :
     `curl -sS https://raw.githubusercontent.com/Gendron-Fils/vesta-tools/main/plugins/outils-gf/commands/chercher.md`
2. **Exécute-la telle qu'elle est écrite**, avec le sujet de Philippe comme `$ARGUMENTS`. Elle
   porte tout : comment formuler la requête (deux ou trois mots-clés, jamais une phrase), où
   sont les secrets, l'appel à l'index, et quoi faire des résultats.
3. **Si tu ne peux pas la lire** (pas de shell, pas de réseau) : dis-le franchement en une
   ligne, puis repêche autrement (les pointeurs d'`etat-courant.md`, les journaux datés du
   dossier `operations/journal-conversations/`). Ne fais jamais semblant d'avoir cherché.

Ne réponds jamais « commande indisponible » : la définition est le contrat, le slash n'est que
le raccourci.
