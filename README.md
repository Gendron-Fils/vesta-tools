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
            └── mission.md        # la commande /mission
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

Le script recopie toutes les commandes de `outils-gf` vers le `.claude/commands/` des dépôts branchés (il trouve les dépôts à côté de `vesta-tools`, en local comme dans le nuage). Le cerveau `vesta` est volontairement exclu (pointeur seulement). Il est additif et idempotent : il ajoute et met à jour, jamais ne supprime. Après coup, committer le `.claude/commands/` de chaque dépôt modifié et ouvrir une PR vers `main` (le script affiche la liste des dépôts touchés).

## Voix et règle d'or

Français québécois, pas de tiret cadratin dans la prose. **Public : aucun secret, aucun contenu propriétaire.** Si un outil aurait besoin d'un secret ou de contenu d'un client, il n'a pas sa place ici.
