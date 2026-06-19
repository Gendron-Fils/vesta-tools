---
description: Clôt la conversation : fait la routine de fin de session (mémoire, validation, backlog, rétro) puis archive un récap daté committé
argument-hint: [sujet optionnel pour cibler le récap d'archive]
---

La conversation est terminée. Fais la routine de fin de session selon les conventions de CE dépôt (son `CLAUDE.md` et la mémoire versionnée qu'il référence), puis archive un récap. Français québécois, factuel, pas de tiret cadratin dans la prose.

Avant d'écrire quoi que ce soit, vérifie l'état réel (la mémoire à jour, ce qui est déjà committé) pour ne pas créer de doublon. Ne pose un geste que si le dépôt a la convention correspondante ; sinon, dis-le et propose plutôt que d'inventer.

## 1. Mémoire
Si une décision stratégique a été prise, inscris-la dans la mémoire évolutive du dépôt (l'état courant ou le backlog selon la convention).

## 2. Tâches et décisions pour l'humain
Si la conversation a laissé à l'humain des choses à faire ou à trancher (une action à poser, du matériel à relire, une décision à prendre), ajoute-les à la file que le dépôt utilise déjà pour ça, celle qui alimente son tableau de bord. Une entrée par item : date, quoi faire ou quoi regarder, et le pointeur vers le document. N'invente pas de nouvelle liste si le dépôt en a déjà une.

## 3. Backlog
Dépose les « à penser plus tard » de la conversation dans la boîte d'entrée du backlog, datés.

## 4. Rétrospective
Si c'était un mandat de conception ou de construction significatif, dépose une rétrospective dans le journal prévu, et promeus vers la charte ce qui se confirme. Si c'est déjà fait dans la conversation, ne le refais pas.

## 5. Commit
Commit le tout avec des messages clairs.

## 6. Archive
Produis un récap daté de la conversation (façon `/recap` : ce qu'on a fait, les décisions, les questions en suspens, la prochaine action) et committe-le dans le journal de conversations de la mémoire versionnée, en créant la convention si elle n'existe pas (par exemple `operations/journal-conversations/AAAA-MM-DD-sujet.md`). Le but : garder une trace durable et cherchable de l'échange, pas seulement les deltas de mémoire.

## 7. Tout sur main
À la clôture, l'humain s'attend à ce que **tout ce qui a été produit dans la conversation finisse sur `main`** : tous les changements committés, et toutes les branches ouvertes pendant la conversation intégrées sur `main`, dans chaque dépôt touché. Rien ne reste en plan sur une branche de travail.

C'est la dernière étape, après l'archive, pour que le récap parte lui aussi sur `main`. Pour chaque dépôt touché dans la session :

- Tire `main` d'abord pour intégrer toute divergence et résoudre les conflits, puis amène la branche de travail sur `main` selon la convention du dépôt : commit direct et merge là où c'est l'usage (la mémoire versionnée), ou PR menée jusqu'au merge là où le dépôt l'exige (les dépôts de code). L'état visé est le même partout : `main` contient tout.
- Pousse `main`, puis vérifie que `main` et la branche pointent sur le même commit et que l'arbre est propre.
- Ne laisse aucune branche ouverte non intégrée, ni aucun changement non committé.

Si un sujet est donné en argument ($ARGUMENTS), cible le récap d'archive là-dessus.

À la fin, dis en clair à l'humain ce qui a été écrit et où, sur quels dépôts `main` a été mis à jour, et ce qui reste à valider de son côté.
