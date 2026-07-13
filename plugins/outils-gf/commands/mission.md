---
description: Prépare ou exécute un ordre de mission. Sans cible existante, rédige un nouvel ordre de mission pour déléguer un bout de travail à un autre agent et produit la ligne de lancement à donner. Avec un fichier d'ordre existant, lit et exécute la mission au complet jusqu'à la rétrospective.
argument-hint: [chemin d'un ordre existant à exécuter | description du bout à déléguer]
---

`/mission` a deux usages. Lis $ARGUMENTS pour savoir lequel :

- **L'argument pointe vers un fichier d'ordre de mission existant** : mode exécuter (section A).
- **Sinon** (une description d'un bout de travail à déléguer, un slug, ou rien dans une conversation où un découpage parallèle vient d'émerger) : mode rédiger (section B).

Français québécois, factuel, pas de tiret cadratin dans la prose.

## A. Exécuter un ordre existant

### 1. Situe la mission
Repère le fichier d'ordre désigné. S'il vit dans un autre dépôt ou sur une autre branche que la session courante, va l'y chercher (tire le dépôt au besoin) avant de commencer. Chemin introuvable ou ambigu : arrête-toi et demande, plutôt que d'inventer une mission.

### 2. Charge le contexte et le persona
Avant d'agir, lis ce que la mission te dit de lire et adopte le persona de développement du dépôt s'il en définit un : sa charte de firme, ses conventions dans le `CLAUDE.md`, la mémoire versionnée qu'il référence. L'ordre de mission est la source : son modèle recommandé, son périmètre, ses garde-fous et sa définition de « fini » priment. Tu t'adaptes à l'état réel du dépôt sur sa branche, jamais l'inverse.

### 3. Exécute au complet
Suis la mission de bout en bout, dans l'ordre qu'elle pose (le risque le plus haut d'abord si elle le demande). Respecte la discipline du dépôt : worktree et PR quand c'est la règle, commits clairs (conventional commits avec le trailer prévu), migrations additives et idempotentes, jamais de destructif sans autorisation. Un secret dans le diff bloque tout. Quand la mission tranche déjà une décision, applique-la ; quand une vraie ambiguïté hors périmètre surgit, expose le risque et demande avant d'agir.

### 4. Ferme la boucle (la rétrospective, et la tâche qui t'a lancé)
Une mission n'est pas finie tant que la rétrospective n'est pas écrite. Dépose-la à l'endroit prévu par le dépôt (le journal de rétrospectives de sa firme de développement) et promeus vers la charte ce qui se confirme. Inscris aussi ce que les conventions demandent : file de validation pour ce qu'un humain devrait relire, backlog pour les « à penser plus tard », datés. Puis ferme la tâche de lancement : si un item de tâche t'a lancé (ton prompt le nomme), ou si un item ouvert de la file porte un `## Prompt de lancement` qui vise ce fichier d'ordre, flippe-le dans la même passe de mémoire (statut selon le contrat du dossier, section de validation avec les références : PR, commit, récap). Une mission exécutée dont la carte reste « à faire » est une tâche zombie au tableau de l'humain.

### 5. Rends compte
Dis en clair ce qui a été livré, ce qui a été committé et où, ce qui reste à valider du côté humain, la prochaine action recommandée. Reprends la définition de « fini » point par point et confirme chaque élément avant de te déclarer arrivé.

## B. Rédiger un nouvel ordre de mission (déléguer)

Le contexte typique : dans la conversation, un bout de travail se détache et pourrait avancer en parallèle, mené par un autre agent. Tu en fais un ordre de mission autoportant, parce que l'agent qui le recevra ne voit pas cette conversation. L'argument, s'il y en a un, cible le bout à déléguer ; sinon, prends le découpage qui vient d'émerger dans l'échange.

### 1. Cerne le mandat
Remonte au pourquoi avant d'écrire. Découpe un périmètre net qui n'entre pas en collision avec le travail en cours (un autre agent va y toucher en même temps). Si le découpage est ambigu, propose-le et fais-le confirmer avant de rédiger.

### 2. Rédige l'ordre selon le gabarit de la firme du dépôt
Un ordre autoportant porte, dans la voix et les conventions du dépôt :

- **l'amorce et le persona** que le dépôt définit pour ses agents (lue depuis sa charte de firme), et la règle de collaboration ;
- **le pourquoi** du mandat, puis **ce qu'on bâtit** ;
- **l'état réel à vérifier au démarrage** (l'agent part de l'état du dépôt sur sa branche, pas d'une supposition) ;
- **la séquence** de travail, avec la discipline du dépôt (worktree et PR, mode plan si la règle le veut) ;
- **les garde-fous** (périmètre d'écriture, secrets, réversibilité, conformité) ;
- **la définition de « fini »**, et **la rétrospective à déposer à la fin**.

Embarque verbatim tout contexte que l'agent ne pourra pas voir autrement (le pont entre la conversation et le dépôt). Ajoute la traçabilité (préparé par qui, quand) et le modèle recommandé (effort, niveau de risque).

### 3. Sauvegarde et committe
Dépose le fichier à l'endroit conventionnel du dépôt pour les ordres de mission (un dossier `prompts/` ou l'équivalent), sous un nom descriptif, et committe-le. Si la convention n'existe pas, propose l'emplacement plutôt que d'inventer en silence.

### 4. Dispatche et pilote (le défaut), ligne de lancement en repli
Par défaut, ne te contente pas de tendre un prompt à coller : la session courante dispatche elle-même la mission à un sous-agent et la pilote. Un sous-agent par mission (une tâche, une branche, une PR), au modèle recommandé dans l'en-tête. Dispatche en parallèle les missions qui ne se chevauchent pas ; garde pour la fin celle qui doit attendre une autre ou entrerait en collision. Pour une mission structurelle ou risquée (URL publiques, schéma, argent, suppression, irréversible), le sous-agent s'arrête à son plan et te le remonte ; tu le relaies à l'humain et tu attends son GO avant de dire « continue ». Une mission réversible à faible risque roule d'un trait jusqu'à la PR et au merge.

Garde toujours le repli : le fichier déposé et la courte ligne de lancement, pour un lancement manuel quand l'humain préfère, ou quand l'environnement courant n'atteint pas la cible (par exemple une mission strictement locale lancée depuis le nuage). Forme de la ligne :

> `[persona d'amorce du dépôt]. Lis et exécute la mission [chemin du fichier créé] dans le dépôt [org/dépôt] (branche [branche]). Suis-la au complet, y compris la rétrospective à la fin.`

Quand le lancement revient à l'humain (mission à lancer en local, préparée depuis le nuage), ne laisse jamais la ligne enterrée dans un récap : crée l'item de tâche selon le contrat de la file de validation de la mémoire (`Type : action`, ligne `Lancement : <modèle>, effort <niveau>`, section `## Prompt de lancement` avec le prompt verbatim et autoportant). Le tableau rend ce prompt avec un bouton Copier ; c'est là que l'humain vient le chercher. Termine toujours le prompt par l'instruction de fermer ce même item à la fin de la mission (le chemin exact du fichier-item), pour que la carte ne survive pas au travail accompli.

### 5. Rends compte
Dis où le fichier est rangé, quelles missions ont été dispatchées et leur état (en cours, en attente du GO de l'humain sur un plan, ou à lancer à la main), donne la ligne de lancement en repli, et signale ce qui reste à décider.
