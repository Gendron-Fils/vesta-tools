---
description: Clôt la conversation : routine de fin de session (mémoire, backlog, rétro, récap archivé), puis tranche les décisions avec toi sur-le-champ
argument-hint: [sujet optionnel pour cibler le récap d'archive]
---

La conversation est terminée. Fais la routine de fin de session selon les conventions de CE dépôt (son `CLAUDE.md` et la mémoire versionnée qu'il référence), puis tranche les décisions avec Philippe et archive un récap. Français québécois, factuel, pas de tiret cadratin dans la prose.

Avant d'écrire quoi que ce soit, vérifie l'état réel (la mémoire à jour, ce qui est déjà committé) pour ne pas créer de doublon. Ne pose un geste que si le dépôt a la convention correspondante ; sinon, dis-le et propose plutôt que d'inventer.

## 1. Mémoire
Si une décision stratégique a été prise, inscris-la dans la mémoire évolutive du dépôt (l'état courant ou le backlog selon la convention).

## 2. Backlog
Dépose les « à penser plus tard » de la conversation dans la boîte d'entrée du backlog, datés.

## 3. Tâches (les gestes qui restent à Philippe)
Les gestes concrets qui restent à Philippe à la fin de la conversation (un verbe : activer, envoyer, cliquer, commander) deviennent des tâches sur son tableau Vesta : un item `Type : action` par geste dans la file de validation de la mémoire, selon le contrat de format du `_LISEZ-MOI.md` du dossier (la commande `/tache` de la boîte fait exactement ça ; sa définition est la routine à suivre). Deux exclusions. Le geste conditionnel à un événement futur va au backlog avec son déclencheur nommé : une tâche affichée qu'il ne peut pas encore poser est du bruit. Et la question de jugement (ses mots, l'argent, la stratégie, le matériel public) reste une validation, jamais une tâche. Pas de doublon avec un item déjà ouvert.

## 4. Péremption (la file reste vraie)
Confronte les items ouverts de la file de validation de la mémoire (tâches comme validations) aux décisions et changements de cap de la conversation. Les noms de fichiers portent le sujet : balaie les titres, et ne lis au complet que les items plausiblement touchés ; ne relis pas toute la file à chaque clôture. Trois issues possibles. Un item périmé par une décision se ferme (`Statut : périmé le AAAA-MM-DD`, plus une courte section qui nomme la décision et pointe où elle est écrite). Un item que la conversation vient de trancher se marque validé selon le contrat du dossier. Des items devenus redondants se regroupent sous un seul, avec pointeurs. Jamais de suppression de fichier, et dans le doute on ne ferme rien : nomme l'item ambigu à l'étape « Trancher avec Philippe » pour qu'il décide. Le but : le tableau reste vrai sans ménage manuel.

## 5. Rétrospective
Si c'était un mandat de conception ou de construction significatif, dépose une rétrospective dans le journal prévu, et promeus vers la charte ce qui se confirme. Si c'est déjà fait dans la conversation, ne le refais pas.

## 6. Commit
Commit le tout avec des messages clairs.

## 7. Archive
Produis un récap daté de la conversation (façon `/recap` : ce qu'on a fait, les décisions, les questions en suspens, la prochaine action) et committe-le dans le journal de conversations de la mémoire versionnée, en créant la convention si elle n'existe pas (par exemple `operations/journal-conversations/AAAA-MM-DD-sujet.md`). Le but : garder une trace durable et cherchable de l'échange, pas seulement les deltas de mémoire.

## 8. Tout sur main, en silence
Tout ce qui a été produit doit finir sur `main` : changements committés, branches de travail intégrées, dans chaque dépôt touché. Pour chaque dépôt touché : tire `main` d'abord pour intégrer toute divergence et résoudre les conflits, puis amène la branche sur `main` selon la convention du dépôt (commit direct et merge pour la mémoire versionnée, PR menée jusqu'au merge pour les dépôts de code), pousse, et vérifie que `main` et la branche pointent sur le même commit et que l'arbre est propre.

C'est de la plomberie : la routine la fait, elle ne la raconte pas. Le message final ne liste ni les dépôts, ni les commits, ni les branches réconciliées. Seule exception qui se signale : une clôture qui a **échoué** quelque part (dépôt non réconcilié, conflit non résolu). Ça, c'est un problème, pas de la plomberie réussie, et Philippe doit le voir sans avoir à demander.

## 9. Trancher avec Philippe, puis le rendu final

Rassemble ce qui requiert le jugement de Philippe et classe chaque item en deux familles.

**Tranchable sur-le-champ** : un choix net dont le rendu tient dans le chat. Pose-le avec l'outil AskUserQuestion, une question par décision, options claires, et **toujours une dernière option « Reporter à plus tard »**. Regroupe plusieurs décisions dans un même appel (jusqu'à quatre questions) pour ne pas mitrailler Philippe un bouton à la fois.
- S'il tranche : applique la décision dans la foulée (mémoire, fichier concerné, item de la file marqué validé) et committe. La boucle se ferme tout de suite.
- S'il choisit « Reporter » : dépose dans la file à valider (une décision en attente) ou le backlog (une idée), daté, avec le pointeur. Rien ne se perd.

**Exige un vrai rendu ou un tiers** : matériel public à voir sur un aperçu Vercel, libellé juridique à faire valider par l'avocat. Ça ne se tranche pas sur un bouton. Dépose dans la file avec le lien du rendu, jamais le fichier brut.

Une fois les questions posées et les réponses appliquées, écris le **message final**, et rien d'autre :

- **✅ Réglé** : en une ou deux puces, ce qui s'est tranché et appliqué dans cette clôture (les décisions que Philippe vient de prendre, le livrable de substance). Confirmation de fond, pas la plomberie : aucune liste de dépôts ni de commits.
- **👉 À toi** : ce qui reste en attente (les tâches posées au tableau à l'étape 3, le reporté, l'en-file parce que ça demande un rendu ou l'avocat). Chaque item : quoi, pourquoi ça a besoin de lui en une ligne, et le lien. Si rien n'attend, le dire en une ligne.
- **➡️ Prochaine action** : une seule, la plus utile.

Garde les emojis sobres, un par titre de section, comme ancres de scan sur cellulaire.

Si un sujet est donné en argument ($ARGUMENTS), cible le récap d'archive là-dessus.
