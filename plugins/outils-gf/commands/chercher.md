---
description: Cherche un sujet dans la mémoire évolutive (index plein-texte de Vesta), pour le repêchage au rituel de session
argument-hint: [mots-clés ou sujet à repêcher]
---

Tu cherches un sujet dans la mémoire évolutive de l'entreprise (le dépôt `vesta`), via son index plein-texte. Ça sert le rituel de repêchage : avant de bâtir sur un sujet, on retrouve les fils déjà au carnet, parce que le modèle est amnésique et qu'un `grep` rate un fil quand on ne devine pas le bon mot. L'index classe par pertinence (plein-texte Postgres, config française), bien mieux que la recherche de code GitHub, et il fonctionne même quand la session n'a pas le dépôt `vesta` cloné (le cas fréquent en session infonuagique scopée sur un dépôt d'outil).

Le sujet à chercher est dans `$ARGUMENTS`. S'il est vide, demande quoi chercher en une ligne, puis arrête.

## Comment chercher

L'index vit dans `vesta-app`, exposé par l'endpoint `POST https://vesta.gendronfils.ca/api/chercher`. Deux secrets, jamais affichés au chat ni écrits dans une réponse :

- le jeton de lecture dédié `VESTA_CHERCHER_TOKEN` (il n'ouvre que cette route, jamais les crons) ;
- le contournement de protection Vercel `VERCEL_AUTOMATION_BYPASS_SECRET`, requis tant que la protection de déploiement est active sur la prod.

Résolution des secrets, dans cet ordre :

1. **Variables d'environnement** (le canal des sessions infonuagiques : posées dans la config de l'environnement Claude Code, valeurs maîtres dans Doppler) : `VESTA_CHERCHER_TOKEN` et `VERCEL_AUTOMATION_BYPASS_SECRET`.
2. **Repli local** (machine de Philippe) : les fichiers `.secrets/vesta-chercher-token.txt` et `.secrets/vesta-vercel-bypass.txt` du dossier Gendron & Fils.

Lis-les depuis bash et utilise-les directement dans la commande `curl`, sans les faire transiter par le chat :

```bash
JETON="${VESTA_CHERCHER_TOKEN:-$(cat ".secrets/vesta-chercher-token.txt" 2>/dev/null)}"
BYPASS="${VERCEL_AUTOMATION_BYPASS_SECRET:-$(cat ".secrets/vesta-vercel-bypass.txt" 2>/dev/null)}"
curl -sS -X POST "https://vesta.gendronfils.ca/api/chercher" \
  -H "Authorization: Bearer ${JETON}" \
  -H "x-vercel-protection-bypass: ${BYPASS}" \
  -H "Content-Type: application/json" \
  --data "$(jq -nc --arg q "$ARGUMENTS" '{question:$q}')"
```

La réponse est `{ "resultats": [ { "chemin": "...", "extrait": "..." }, ... ] }`, déjà classée du plus pertinent au moins.

## Quoi en faire

1. Présente les résultats : pour chacun, le chemin et l'extrait surligné, du plus pertinent au moins. Quelques-uns, pas la liste brute complète.
2. Ouvre les fichiers les plus pertinents pour bâtir ta réponse sur le vrai contenu, pas seulement l'extrait : depuis le clone local de la mémoire s'il est dans la session, sinon par l'API GitHub (`Gendron-Fils/vesta`).
3. Si l'index ne rend rien ou que l'endpoint est injoignable (secrets absents, réseau) : dis-le franchement et dégrade proprement. Si le dépôt `vesta` est cloné dans la session, retombe sur une recherche locale (`rg -i`) en le signalant ; sinon, dis que la recherche de la mémoire n'est pas disponible dans cette session et ce qui manque (la variable d'environnement). Ne fais jamais semblant d'avoir cherché l'index si tu ne l'as pas atteint.

Note : l'index se remplit et se rafraîchit tout seul (cron quotidien `/api/cron/reindex-memoire` à 7 h de l'Est). Les résultats reflètent la mémoire de la dernière réindexation, pas les commits de la dernière heure.
