---
description: Cherche un sujet dans la mémoire évolutive (index plein-texte de Vesta), pour le repêchage au rituel de session
argument-hint: [mots-clés ou sujet à repêcher]
---

Tu cherches un sujet dans la mémoire évolutive de l'entreprise (le dépôt `vesta`), via son index plein-texte. Ça sert le rituel de repêchage : avant de bâtir sur un sujet, on retrouve les fils déjà au carnet, parce que le modèle est amnésique et qu'un `grep` rate un fil quand on ne devine pas le bon mot. L'index classe par pertinence (plein-texte Postgres, config française), bien mieux que la recherche de code GitHub.

Le sujet à chercher est dans `$ARGUMENTS`. S'il est vide, demande quoi chercher en une ligne, puis arrête.

## Comment chercher

L'index vit dans `vesta-app`, exposé par l'endpoint `POST https://vesta.gendronfils.ca/api/chercher`. Deux secrets, lus depuis le dossier `.secrets/` de Gendron & Fils, jamais affichés au chat ni écrits dans une réponse :

- le jeton d'automatisation (`CRON_SECRET`), dans `.secrets/vesta-cron-secret.txt` ;
- le contournement de protection Vercel (`VERCEL_AUTOMATION_BYPASS_SECRET`), dans `.secrets/vesta-vercel-bypass.txt`, requis tant que la protection de déploiement est active sur la prod.

Lis ces fichiers depuis bash et utilise-les directement dans la commande `curl`, sans les faire transiter par le chat :

```bash
SECRET="$(cat ".secrets/vesta-cron-secret.txt" 2>/dev/null)"
BYPASS="$(cat ".secrets/vesta-vercel-bypass.txt" 2>/dev/null)"
curl -sS -X POST "https://vesta.gendronfils.ca/api/chercher" \
  -H "Authorization: Bearer ${SECRET}" \
  -H "x-vercel-protection-bypass: ${BYPASS}" \
  -H "Content-Type: application/json" \
  --data "$(jq -nc --arg q "$ARGUMENTS" '{question:$q}')"
```

La réponse est `{ "resultats": [ { "chemin": "...", "extrait": "..." }, ... ] }`, déjà classée du plus pertinent au moins.

## Quoi en faire

1. Présente les résultats : pour chacun, le chemin cliquable et l'extrait surligné, du plus pertinent au moins. Quelques-uns, pas la liste brute complète.
2. Ouvre les fichiers les plus pertinents depuis le clone local de la mémoire (lecture), pour bâtir ta réponse sur le vrai contenu, pas seulement l'extrait.
3. Si l'index ne rend rien (vide parce que pas encore réindexé, ou endpoint injoignable), dis-le franchement et retombe sur une recherche locale (`rg -i` sur le clone de la mémoire) en le signalant. Ne fais jamais semblant d'avoir cherché l'index si tu ne l'as pas atteint.

Note : sans les secrets dans `.secrets/`, ou tant que l'index n'a pas été réindexé une première fois (cron quotidien `/api/cron/reindex-memoire`, ou déclenchement manuel avec le même Bearer), cette commande retombe sur la recherche locale. C'est non cassant : elle dégrade proprement, elle ne ment pas.
