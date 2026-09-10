# vesta-tools

La boîte à outils Claude Code partagée de Gendron & Fils. On définit une commande **une seule fois** ici, et tous les dépôts branchés la voient, sans dupliquer de fichier.

Ce dépôt est **public** exprès : les sessions Claude Code dans le nuage (conteneur éphémère) le clonent sans jeton. Conséquence directe : **rien de sensible n'entre ici**, jamais de secret, jamais de contenu propriétaire. Seulement des commandes génériques.

## Ce qu'il y a dedans

C'est un *marketplace* de plugins Claude Code qui contient un plugin :

```
vesta-tools/
├── .claude-plugin/
│   └── marketplace.json          # le catalogue, nom « gendron-tools »
└── plugins/
    └── outils-gf/                # le plugin, nom « outils-gf »
        ├── .claude-plugin/
        │   └── plugin.json
        └── commands/
            ├── recap.md          # la commande /recap
            ├── closing-time.md   # la commande /closing-time
            ├── mission.md        # la commande /mission
            ├── chercher.md       # la commande /chercher
            ├── tache.md          # la commande /tache
            └── jazz.md           # la commande /jazz
```

Plus un dossier de skills, le canal qui va partout (voir plus bas) :

```
vesta-tools/
└── skills/
    ├── chercher/SKILL.md         # pointeur vers commands/chercher.md
    └── mission/SKILL.md          # pointeur vers commands/mission.md
```

- **Marketplace** : `gendron-tools`
- **Plugin** : `outils-gf`
- **Référence d'un dépôt** vers le plugin : `outils-gf@gendron-tools`

## Brancher un dépôt sur la boîte

Trois lignes à fusionner dans le `.claude/settings.json` du dépôt (créer le fichier s'il n'existe pas) :

```json
{
  "extraKnownMarketplaces": {
    "gendron-tools": { "source": { "source": "github", "repo": "Gendron-Fils/vesta-tools" } }
  },
  "enabledPlugins": { "outils-gf@gendron-tools": true }
}
```

Si le dépôt a déjà un `.claude/settings.json`, on **fusionne** ces deux clés dedans, on n'écrase pas le reste.

Note sur le nuage : la doc Claude Code indique qu'un plugin déclaré ainsi est **proposé à l'installation** quand on fait confiance au dossier du dépôt (ce n'est pas toujours un chargement silencieux). Si une session nuage fraîche ne charge pas le plugin sans invite, le filet est un `.claude/commands/recap.md` committé dans le dépôt (voir le compte rendu de mise en place).

Note sur le nom de la commande : les commandes de plugin sont **préfixées par le nom du plugin**. La commande s'invoque donc `/outils-gf:recap`. Un fichier local `.claude/commands/recap.md` donne, lui, le `/recap` court.

## Ajouter un outil plus tard

Le geste de base est unique : déposer **un fichier de plus** dans `plugins/outils-gf/commands/` (par exemple `monday-brief.md`), committer, pousser sur `main`. Côté plugin, tous les dépôts branchés le voient au prochain démarrage de session (un rafraîchissement du marketplace peut être nécessaire).

Pour aussi propager le filet committé qui garantit la commande dans les sessions nuage, lancer le script de synchronisation depuis ce dépôt :

```bash
scripts/sync-commands.sh --dry-run   # aperçu : montre ce qui changerait
scripts/sync-commands.sh             # recopie dans le .claude/commands/ des dépôts branchés
```

Le script recopie toutes les commandes de `outils-gf` vers le `.claude/commands/` des dépôts branchés (il trouve les dépôts à côté de `vesta-tools`, en local comme dans le nuage). La mémoire `vesta` est volontairement exclue (pointeur seulement). Elle est additive et idempotente : elle ajoute et met à jour, jamais ne supprime. Après coup, committer le `.claude/commands/` de chaque dépôt modifié et ouvrir une PR vers `main` (le script affiche la liste des dépôts touchés).

## Trois canaux de distribution (et lequel va partout)

Une commande de la boîte peut atteindre une session par trois chemins, et **un seul des trois
va partout** :

| Canal | Où ça vit | Surfaces couvertes |
|---|---|---|
| Plugin `outils-gf` | le `settings.json` de la machine | **app de bureau seulement** |
| Copie vendorisée | le `.claude/commands/` d'un dépôt d'outil | **sessions infonuagiques de CE dépôt** |
| Skill de compte | le compte claude.ai | **partout** : mobile, infonuagique, bureau |

Le `settings.json` d'une machine ne monte pas dans un conteneur infonuagique, et la mémoire
`vesta` ne vendorise rien (elle reste pointeur seulement). Une session mobile ou infonuagique
ouverte sur `vesta` n'expose donc **aucune** commande du plugin : elle rend `Unknown command`.

Le filet existe déjà et il est automatique : l'`AGENTS.md` de `vesta` instruit toute session de
lire la définition maîtresse ici et de l'exécuter. **La définition est le contrat, le slash
n'est que le raccourci.** Le filet fait le travail, mais il ne fait pas disparaître l'erreur
rouge que Philippe voit quand il tape la commande.

D'où le dossier `skills/` : pour les commandes que Philippe tape lui-même sur mobile, un skill
de compte porte le nom de la commande sur toutes les surfaces. **Ces skills sont des pointeurs,
jamais des copies** : leur corps dit d'aller lire `plugins/outils-gf/commands/<nom>.md` et
d'exécuter la routine. Une seule source, aucune divergence possible, et la CI vérifie que le
pointeur vise un fichier qui existe.

Pourquoi deux et pas les six : chaque skill de compte coûte sa description au démarrage de
**chaque** session, sur toutes les surfaces, y compris celles où le plugin fait déjà la job
(audit token du 2026-07-17). On ne paie ce coût que là où le geste lui-même est en jeu, pas pour
le confort. Deux cas le justifient :

- **`/chercher`** (posé le 2026-09-09) : c'est un réflexe en ancrage, et l'erreur rouge
  déconditionne le geste au moment exact où Philippe le pratique.
- **`/mission`** (converti le 2026-09-10) : le skill existait déjà, mais en COPIE depuis le
  2026-05-29 ; il n'est pas ajouté ici, il est remis en pointeur pour tuer la dérive.

`/closing-time` avait été fait dans la même passe que `/chercher` puis retiré le 2026-09-09, à la
demande de Philippe : la commande est bien absente de ces surfaces elle aussi, mais la clôture se
fait très bien par le filet, personne n'apprend un réflexe à ce moment-là, et un skill de moins
est une description de moins payée à chaque démarrage. Les autres commandes sont dans ce cas : le
filet de l'`AGENTS.md` les couvre.

**Le piège à surveiller : la copie qui dérive.** `/mission` existe dans les deux canaux depuis
le 2026-05-29, et les deux ont divergé (le skill de compte est resté à la version d'avant le
dégraissage de la 0.12.0). C'est exactement ce que la forme pointeur évite. Un skill de compte
qui recopie une routine est une dérive en attente.

### Poser ou mettre à jour un skill de compte

Le téléversement est un geste manuel de Philippe (claude.ai, Réglages, Capacités, Skills).
**Quand un skill du même nom existe déjà, retirer l'ancien AVANT de poser le nouveau**, sinon
deux skills homonymes peuvent cohabiter. Le repli pendant l'opération est sûr : le plugin
continue de servir la commande au bureau, et le filet de l'`AGENTS.md` la couvre ailleurs.

Pour fabriquer l'archive à téléverser :

```bash
cd /chemin/vers/vesta-tools/skills && zip -r chercher.zip chercher
```

Le critère avant d'en ajouter un : est-ce que Philippe tape cette commande LUI-MÊME sur une
surface sans plugin, et est-ce que l'échec lui coûte autre chose qu'une seconde ? Si le filet
suffit, le filet suffit.

Une fois posé, le skill se synchronise tout seul vers les autres surfaces.

## Le composeur PDF pour la reMarkable (script, hors plugin)

`scripts/md-vers-pdf-remarkable.py` rend un ou plusieurs fichiers Markdown en un seul PDF au format exact de l'écran d'une reMarkable 2 (447 × 597 points), avec Chromium ou Chrome sans tête. Aucune dépendance Python ; il trouve le navigateur tout seul (Playwright dans le nuage, Chrome sur Windows ou macOS, sinon `CHROMIUM_BIN` ou `--chromium CHEMIN`). C'est un script, pas une commande du plugin : une session l'appelle depuis le clone de `vesta-tools`.

```bash
python3 scripts/md-vers-pdf-remarkable.py --sortie sortie.pdf document.md
python3 scripts/md-vers-pdf-remarkable.py --sortie sortie.pdf --suivre-liens --titre-annexe "Les fiches liées" edition.md
```

`--suivre-liens` ajoute en annexe, une fois chacun, les fichiers `.md` locaux que le document lie ; `--bandeau` pose une ligne en tête ; `--html` garde le HTML intermédiaire pour déboguer. Le rendu vise l'encre : sérif, noir pur, marges franches, titres qui ne se séparent pas de leur paragraphe. Il n'imprime que des chemins et des comptes, jamais de contenu.

## Voix et règle d'or

Français québécois, pas de tiret cadratin dans la prose. **Public : aucun secret, aucun contenu propriétaire.** Si un outil aurait besoin d'un secret ou de contenu d'un client, il n'a pas sa place ici.
