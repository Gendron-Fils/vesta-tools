#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
md-vers-pdf-remarkable.py : rend un ou plusieurs fichiers Markdown en UN PDF au
format exact de l'écran d'une reMarkable 2 (447 x 597 points, soit 1404 x 1872
pixels à 226 ppp), avec Chromium ou Chrome sans tête. Aucune dépendance Python.

Pourquoi : un document poussé sur la tablette se lit sans zoom seulement s'il a
la taille de l'écran. Le rendu de marque est invisible sur de l'encre en niveaux
de gris ; ce composeur vise la lisibilité (sérif, marges franches, noir pur).

Usage :
  python3 md-vers-pdf-remarkable.py --sortie sortie.pdf fichier.md [autre.md ...]

Options :
  --sortie CHEMIN        le PDF à écrire (obligatoire)
  --suivre-liens         ajoute en annexe, une fois chacun, les fichiers .md
                         locaux liés depuis les fichiers donnés (un lien
                         [texte](chemin.md) relatif au fichier qui le porte)
  --titre-annexe TEXTE   titre de la page qui ouvre l'annexe (défaut : « Annexe »)
  --bandeau TEXTE        une ligne en tête de la première page (ex. le nom du
                         journal), vide par défaut
  --html CHEMIN          écrit aussi le HTML intermédiaire (pour déboguer)
  --chromium CHEMIN      le binaire à utiliser ; sinon CHROMIUM_BIN, puis les
                         emplacements connus (Playwright, Linux, Windows, macOS)

Sous-ensemble Markdown couvert : titres # à ####, paragraphes, listes à puces et
numérotées (deux niveaux), citations >, blocs de code ```, tableaux |, lignes
horizontales ---, gras, italique, code en ligne, liens. Un paragraphe entièrement
en italique (une ligne de source, une note) se rend plus petit ; des lignes
consécutives « Clé : valeur » (Numéro, Slug, Mis à jour le) restent chacune sur
leur ligne. Ce qui n'est pas
couvert se rend en texte brut : le composeur ne plante jamais sur du contenu.

Codes de sortie : 0 rendu ; 1 mauvais usage ou fichier introuvable ; 2 Chromium
introuvable ; 3 Chromium a échoué. N'imprime que des chemins et des comptes.
"""

import argparse
import glob
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile

LARGEUR_PT = 447
HAUTEUR_PT = 597

# ----------------------------------------------------------------------------
# Markdown : un convertisseur minimal, tolérant, sans dépendance.
# ----------------------------------------------------------------------------

RE_TITRE = re.compile(r"^(#{1,4})\s+(.*?)\s*#*\s*$")
RE_PUCE = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")
RE_CITATION = re.compile(r"^>\s?(.*)$")
RE_REGLE = re.compile(r"^\s*([-*_])(\s*\1){2,}\s*$")
RE_TABLEAU_SEP = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")
RE_LIEN = re.compile(r"\[([^\]]+)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
RE_CODE = re.compile(r"`([^`]+)`")
RE_GRAS = re.compile(r"\*\*(.+?)\*\*")
RE_ITAL = re.compile(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])")
RE_ITAL_PARA = re.compile(r"^\*(?!\*)(.+)\*$", re.S)
# Une ligne « Clé : valeur » (Numéro, Slug, Mis à jour le, Sources principales...).
RE_CLE_VALEUR = re.compile(r"^[^\s:][^:\n]{0,40}\s:\s\S")


def rendre_inline(texte, liens_trouves=None, base=None):
    """Échappe le HTML puis applique code, gras, italique et liens."""
    texte = html.escape(texte, quote=False)
    codes = []

    def garder_code(m):
        codes.append("<code>%s</code>" % m.group(1))
        return "\x00%d\x00" % (len(codes) - 1)

    texte = RE_CODE.sub(garder_code, texte)

    def lien(m):
        libelle, cible = m.group(1), m.group(2)
        if liens_trouves is not None and cible.lower().endswith(".md") and not cible.startswith(("http://", "https://")):
            chemin = os.path.normpath(os.path.join(base or ".", cible.split("#")[0]))
            if chemin not in liens_trouves:
                liens_trouves.append(chemin)
            return '<a class="local">%s</a>' % libelle
        return '<a href="%s">%s</a>' % (html.escape(cible, quote=True), libelle)

    texte = RE_LIEN.sub(lien, texte)
    texte = RE_GRAS.sub(r"<strong>\1</strong>", texte)
    texte = RE_ITAL.sub(r"<em>\1</em>", texte)
    texte = re.sub(r"\x00(\d+)\x00", lambda m: codes[int(m.group(1))], texte)
    return texte


def rendre_markdown(source, base=None, liens_trouves=None):
    """Rend un document Markdown en HTML. Rend toujours quelque chose."""
    lignes = source.replace("\r\n", "\n").split("\n")
    out = []
    para = []
    i = 0

    def vider_para():
        if para:
            propres = [l.strip() for l in para if l.strip()]
            if len(propres) > 1 and all(RE_CLE_VALEUR.match(l) for l in propres):
                # Des lignes d'en-tête consécutives (Numéro, Semaine couverte, Slug...)
                # restent chacune sur leur ligne au lieu de se fondre en paragraphe.
                out.append('<p class="meta">%s</p>' % "<br>".join(rendre_inline(l, liens_trouves, base) for l in propres))
                para.clear()
                return
            texte = " ".join(propres).strip()
            if texte:
                m = RE_ITAL_PARA.match(texte)
                if m and "*" not in m.group(1):
                    out.append('<p class="note">%s</p>' % rendre_inline(m.group(1), liens_trouves, base))
                else:
                    out.append("<p>%s</p>" % rendre_inline(texte, liens_trouves, base))
            para.clear()

    while i < len(lignes):
        ligne = lignes[i]
        depouillee = ligne.strip()

        # Bloc de code clôturé.
        if depouillee.startswith("```"):
            vider_para()
            bloc = []
            i += 1
            while i < len(lignes) and not lignes[i].strip().startswith("```"):
                bloc.append(lignes[i])
                i += 1
            out.append("<pre>%s</pre>" % html.escape("\n".join(bloc), quote=False))
            i += 1
            continue

        if not depouillee:
            vider_para()
            i += 1
            continue

        m = RE_TITRE.match(ligne)
        if m:
            vider_para()
            niveau = len(m.group(1))
            out.append("<h%d>%s</h%d>" % (niveau, rendre_inline(m.group(2), liens_trouves, base), niveau))
            i += 1
            continue

        if RE_REGLE.match(ligne):
            vider_para()
            out.append("<hr>")
            i += 1
            continue

        if RE_CITATION.match(ligne):
            vider_para()
            bloc = []
            while i < len(lignes) and RE_CITATION.match(lignes[i]):
                bloc.append(RE_CITATION.match(lignes[i]).group(1))
                i += 1
            out.append("<blockquote>%s</blockquote>" % rendre_markdown("\n".join(bloc), base, liens_trouves))
            continue

        if depouillee.startswith("|") and i + 1 < len(lignes) and RE_TABLEAU_SEP.match(lignes[i + 1]):
            vider_para()
            entete = [c.strip() for c in depouillee.strip("|").split("|")]
            i += 2
            rangs = []
            while i < len(lignes) and lignes[i].strip().startswith("|"):
                rangs.append([c.strip() for c in lignes[i].strip().strip("|").split("|")])
                i += 1
            t = ["<table><thead><tr>"]
            t += ["<th>%s</th>" % rendre_inline(c, liens_trouves, base) for c in entete]
            t.append("</tr></thead><tbody>")
            for r in rangs:
                t.append("<tr>" + "".join("<td>%s</td>" % rendre_inline(c, liens_trouves, base) for c in r) + "</tr>")
            t.append("</tbody></table>")
            out.append("".join(t))
            continue

        m = RE_PUCE.match(ligne)
        if m:
            vider_para()
            pile = []  # [(indentation, balise)]
            while i < len(lignes):
                m = RE_PUCE.match(lignes[i])
                if not m:
                    # Une ligne de continuation indentée reste dans l'item courant.
                    if lignes[i].strip() and lignes[i].startswith((" ", "\t")) and pile:
                        out.append(" " + rendre_inline(lignes[i].strip(), liens_trouves, base))
                        i += 1
                        continue
                    break
                indent = len(m.group(1).expandtabs(4))
                balise = "ol" if m.group(2)[0].isdigit() else "ul"
                while pile and indent < pile[-1][0]:
                    out.append("</li></%s>" % pile.pop()[1])
                if not pile or indent > pile[-1][0]:
                    pile.append((indent, balise))
                    out.append("<%s><li>" % balise)
                else:
                    out.append("</li><li>")
                out.append(rendre_inline(m.group(3), liens_trouves, base))
                i += 1
            while pile:
                out.append("</li></%s>" % pile.pop()[1])
            continue

        para.append(ligne)
        i += 1

    vider_para()
    return "\n".join(out)


# ----------------------------------------------------------------------------
# La page : feuille de style pensée pour l'encre, format de l'écran.
# ----------------------------------------------------------------------------

STYLE = """
@page { size: %dpt %dpt; margin: 26pt 28pt 30pt 28pt; }
html { -webkit-print-color-adjust: exact; }
body { margin: 0; color: #000; background: #fff;
  font-family: "Charter", "Bitstream Charter", "Georgia", "Liberation Serif", "Times New Roman", serif;
  font-size: 10.5pt; line-height: 1.42; }
.bandeau { font-size: 8.5pt; letter-spacing: 0.12em; text-transform: uppercase;
  border-bottom: 0.75pt solid #000; padding-bottom: 4pt; margin-bottom: 14pt; }
section.doc { page-break-before: always; break-before: page; }
section.doc:first-of-type { page-break-before: auto; break-before: auto; }
h1 { font-size: 18pt; line-height: 1.2; margin: 0 0 10pt 0; break-after: avoid; }
h2 { font-size: 13.5pt; line-height: 1.25; margin: 18pt 0 6pt 0; padding-top: 6pt;
  border-top: 0.75pt solid #000; break-after: avoid; }
h3 { font-size: 11.5pt; line-height: 1.3; margin: 12pt 0 4pt 0; break-after: avoid; }
h4 { font-size: 10.5pt; margin: 10pt 0 3pt 0; break-after: avoid; }
p { margin: 0 0 7pt 0; orphans: 2; widows: 2; text-align: left; hyphens: manual; }
p.meta { font-size: 9pt; line-height: 1.4; margin-bottom: 9pt; }
p.note { font-size: 9pt; line-height: 1.35; color: #000; margin-bottom: 9pt; }
ul, ol { margin: 0 0 7pt 0; padding-left: 16pt; }
li { margin-bottom: 3pt; }
blockquote { margin: 0 0 8pt 0; padding: 2pt 0 2pt 9pt; border-left: 1.5pt solid #000; }
blockquote p:last-child { margin-bottom: 0; }
code { font-family: "Liberation Mono", "DejaVu Sans Mono", "Consolas", "Courier New", monospace;
  font-size: 9pt; }
pre { font-family: "Liberation Mono", "DejaVu Sans Mono", "Consolas", "Courier New", monospace;
  font-size: 8pt; line-height: 1.3; white-space: pre-wrap; word-break: break-word;
  border: 0.5pt solid #000; padding: 5pt; margin: 0 0 8pt 0; }
a { color: #000; text-decoration: underline; text-decoration-thickness: 0.6pt; text-underline-offset: 1.5pt; }
a.local { text-decoration-style: dotted; }
hr { border: 0; border-top: 0.5pt solid #000; margin: 10pt 0; }
table { border-collapse: collapse; width: 100%%; margin: 0 0 8pt 0; font-size: 9.5pt; }
th, td { border: 0.5pt solid #000; padding: 3pt 4pt; vertical-align: top; text-align: left; }
th { font-weight: bold; }
.annexe-titre { font-size: 15pt; margin: 0 0 12pt 0; padding-bottom: 6pt; border-bottom: 0.75pt solid #000; }
""" % (LARGEUR_PT, HAUTEUR_PT)


def composer_html(fichiers, bandeau, suivre_liens, titre_annexe):
    """Assemble les documents (et l'annexe des fichiers liés) en une page HTML."""
    sections = []
    liens = []
    titre_pdf = None
    for chemin in fichiers:
        with open(chemin, encoding="utf-8") as f:
            source = f.read()
        if titre_pdf is None:
            m = re.search(r"^#\s+(.+?)\s*$", source, re.M)
            titre_pdf = m.group(1) if m else os.path.basename(chemin)
        corps = rendre_markdown(source, os.path.dirname(chemin), liens if suivre_liens else None)
        sections.append('<section class="doc">%s</section>' % corps)

    annexes = []
    if suivre_liens:
        vus = set(os.path.normpath(f) for f in fichiers)
        for chemin in liens:
            if chemin in vus or not os.path.isfile(chemin):
                continue
            vus.add(chemin)
            with open(chemin, encoding="utf-8") as f:
                corps = rendre_markdown(f.read(), os.path.dirname(chemin), None)
            annexes.append('<section class="doc">%s</section>' % corps)
        if annexes:
            annexes[0] = annexes[0].replace(
                '<section class="doc">',
                '<section class="doc"><p class="annexe-titre">%s</p>' % html.escape(titre_annexe, quote=False), 1)

    tete = ('<div class="bandeau">%s</div>' % html.escape(bandeau, quote=False)) if bandeau else ""
    page = ("<!doctype html><html lang=\"fr\"><head><meta charset=\"utf-8\">"
            "<title>%s</title><style>%s</style></head><body>%s%s%s</body></html>"
            % (html.escape(titre_pdf or "Document", quote=False), STYLE, tete, "\n".join(sections), "\n".join(annexes)))
    return page, len(annexes)


# ----------------------------------------------------------------------------
# Chromium : on le trouve, on l'appelle, on vérifie qu'il a écrit.
# ----------------------------------------------------------------------------

CANDIDATS = [
    "/opt/pw-browsers/chromium-*/chrome-linux/chrome",
    "/opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell",
    "/usr/bin/chromium", "/usr/bin/chromium-browser", "/usr/bin/google-chrome", "/usr/bin/google-chrome-stable",
    "/snap/bin/chromium",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.join(os.environ.get("LOCALAPPDATA", ""), "Google", "Chrome", "Application", "chrome.exe"),
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]


def trouver_chromium(explicite=None):
    if explicite:
        return explicite if os.path.isfile(explicite) else None
    env = os.environ.get("CHROMIUM_BIN")
    if env and os.path.isfile(env):
        return env
    for motif in CANDIDATS:
        for trouve in sorted(glob.glob(motif), reverse=True):
            if os.path.isfile(trouve):
                return trouve
    for nom in ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable", "chrome", "msedge"):
        chemin = shutil.which(nom)
        if chemin:
            return chemin
    return None


def imprimer_pdf(chromium, chemin_html, chemin_pdf):
    url = "file:///" + os.path.abspath(chemin_html).replace("\\", "/").lstrip("/")
    commande = [
        chromium, "--headless=new", "--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage",
        "--no-first-run", "--no-default-browser-check", "--disable-extensions",
        "--no-pdf-header-footer", "--virtual-time-budget=4000",
        "--print-to-pdf=" + os.path.abspath(chemin_pdf), url,
    ]
    resultat = subprocess.run(commande, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=180)
    if resultat.returncode != 0 or not os.path.isfile(chemin_pdf) or os.path.getsize(chemin_pdf) == 0:
        # Le repli du vieux mode sans tête (Chrome < 112).
        commande[1] = "--headless"
        resultat = subprocess.run(commande, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=180)
    if resultat.returncode != 0 or not os.path.isfile(chemin_pdf) or os.path.getsize(chemin_pdf) == 0:
        erreurs = resultat.stderr.decode("utf-8", "replace").strip().splitlines()[-3:]
        raise RuntimeError("Chromium n'a pas écrit le PDF (code %d). %s" % (resultat.returncode, " | ".join(erreurs)))


def compter_pages(chemin_pdf):
    with open(chemin_pdf, "rb") as f:
        donnees = f.read()
    return len(re.findall(rb"/Type\s*/Page[^s]", donnees))


def principal(argv):
    p = argparse.ArgumentParser(description="Rend du Markdown en PDF au format de l'écran reMarkable 2.")
    p.add_argument("fichiers", nargs="+", help="fichier(s) Markdown, dans l'ordre")
    p.add_argument("--sortie", required=True, help="le PDF à écrire")
    p.add_argument("--suivre-liens", action="store_true", help="ajoute en annexe les .md locaux liés")
    p.add_argument("--titre-annexe", default="Annexe")
    p.add_argument("--bandeau", default="")
    p.add_argument("--html", default=None, help="écrit aussi le HTML intermédiaire")
    p.add_argument("--chromium", default=None, help="binaire Chromium ou Chrome")
    args = p.parse_args(argv)

    for f in args.fichiers:
        if not os.path.isfile(f):
            print("Fichier introuvable : %s" % f, file=sys.stderr)
            return 1

    chromium = trouver_chromium(args.chromium)
    if not chromium:
        print("Chromium introuvable : donne --chromium CHEMIN ou pose CHROMIUM_BIN.", file=sys.stderr)
        return 2

    page, n_annexes = composer_html(args.fichiers, args.bandeau, args.suivre_liens, args.titre_annexe)
    dossier_tmp = tempfile.mkdtemp(prefix="md-vers-pdf-")
    chemin_html = os.path.join(dossier_tmp, "page.html")
    with open(chemin_html, "w", encoding="utf-8") as f:
        f.write(page)
    if args.html:
        with open(args.html, "w", encoding="utf-8") as f:
            f.write(page)

    sortie = os.path.abspath(args.sortie)
    os.makedirs(os.path.dirname(sortie) or ".", exist_ok=True)
    try:
        imprimer_pdf(chromium, chemin_html, sortie)
    except (RuntimeError, subprocess.TimeoutExpired) as e:
        print("Rendu échoué : %s" % e, file=sys.stderr)
        return 3
    finally:
        shutil.rmtree(dossier_tmp, ignore_errors=True)

    print("PDF écrit : %s (%d pages, %d octets, %d document(s), %d fiche(s) en annexe)"
          % (sortie, compter_pages(sortie), os.path.getsize(sortie), len(args.fichiers), n_annexes))
    return 0


if __name__ == "__main__":
    sys.exit(principal(sys.argv[1:]))
