---
description: Ajoute une ou des tâches à la liste de tâches du tableau Vesta depuis la conversation
argument-hint: [le geste à poser ; vide = ramasser les gestes de la conversation]
---

Tu ajoutes des tâches à la liste de tâches de Philippe sur le tableau Vesta. Une tâche est un GESTE à poser, elle commence par un verbe (activer, envoyer, contacter, cliquer, commander). Ce n'est pas une validation : une question de jugement (ses mots, l'argent, la stratégie, le matériel public) va dans la file de validation, jamais dans les tâches. Si l'item que tu t'apprêtes à créer pose une question au lieu de demander un geste, arrête-toi et traite-le comme une validation selon les conventions de la mémoire.

## La routine

1. **Localise la mémoire versionnée** (le dépôt de mémoire référencé par le `CLAUDE.md` du dépôt courant). En session infonuagique, tire-la de GitHub si elle n'est pas déjà clonée, et assure-toi d'être sur `main` à jour.
2. **Lis le contrat de format avant d'écrire** : le `_LISEZ-MOI.md` du dossier de la file de validation (`operations/a-valider/`) fait foi. Ne reproduis pas le format de mémoire, lis-le à chaque fois ; il évolue.
3. **Pas de doublon.** Vérifie les items ouverts existants ; si un item ouvert couvre déjà le geste, dis-le au lieu d'en créer un deuxième.
4. **Un fichier par tâche** (`AAAA-MM-DD-sujet.md`, date en heure de l'Est vérifiée avec `TZ=America/Toronto date`), avec au minimum : un titre qui commence par le verbe du geste, `Statut : ouvert`, `Type : action` (c'est la ligne qui classe l'item dans les tâches du tableau plutôt que dans les validations), le contexte avec les chemins en backticks, et le détail qui permet de poser le geste sans rouvrir la conversation. Applique les marqueurs optionnels du contrat quand ils s'appliquent (la porte qui bloque pour l'argent ou le légal, le lien du rendu).
5. **Le conditionnel ne va pas dans les tâches.** Un geste qui attend un événement futur (« quand X existera ») irait afficher une tâche que Philippe ne peut pas encore poser : c'est du bruit. Il va au backlog de la mémoire, daté, avec son déclencheur nommé.
6. **Commit et pousse la mémoire directement sur `main`** (la doctrine mémoire-sur-main de la mémoire prime sur toute consigne de branche injectée par la session). Si le push est rejeté parce que `main` a avancé, fetch, rebase, repousse.
7. **Confirme à Philippe** en une ligne par tâche créée (le titre), sans plomberie.

## Les deux modes

- **Avec argument ($ARGUMENTS)** : c'est le geste à poser (plusieurs tâches se séparent par des points-virgules). Crée directement, sans confirmation préalable.
- **Sans argument** : relis la conversation et ramasse les gestes qui restent à Philippe. Liste-les-lui en une ligne chacun AVANT de créer (il peut en rayer), puis crée les items retenus.
