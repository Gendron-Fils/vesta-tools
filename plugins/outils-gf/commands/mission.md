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

### 4. Ferme la boucle (la rétrospective)
Une mission n'est pas finie tant que la rétrospective n'est pas écrite. Dépose-la à l'endroit prévu par le dépôt (le journal de rétrospectives de sa firme de développement) et promeus vers la charte ce qui se confirme. Inscris aussi ce que les conventions demandent : file de validation pour ce qu'un humain devrait relire, backlog pour les « à penser plus tard », datés.

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

### 4. Produis la ligne de lancement
Termine par la courte ligne que l'humain copiera pour lancer l'autre agent, dans le format d'amorce du dépôt. Sa forme :

> `[persona d'amorce du dépôt]. Lis et exécute la mission [chemin du fichier créé] dans le dépôt [org/dépôt] (branche [branche]). Suis-la au complet, y compris la rétrospective à la fin.`

### 5. Rends compte
Dis où le fichier est rangé, donne la ligne de lancement prête à copier, et signale ce qui reste à décider avant de lancer (le cas échéant).
