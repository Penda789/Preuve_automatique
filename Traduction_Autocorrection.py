#!/usr/bin/env python3
"""
Boucle d'autocorrection complète sur le benchmark :
  1. Appelle trad_enonce() de Traduction_Fr_to_Coq.py (FR → Coq + exécution)
  2. Si Coq OK → lit temp.v → rétrotraduit Coq → FR
  3. Compare sémantiquement FR original vs FR rétrotraduit
  4. Si équivalent → succès
     Sinon → prompt enrichi et nouveau cycle
  5. Lance automatiquement sur BENCHMARK_FACILE, INTERMEDIAIRE, AVANCE
"""

import os
from mistralai.client import Mistral
from Traduction_Fr_to_Coq import trad_enonce
from benchmark_graphes import BENCHMARK_FACILE, BENCHMARK_INTERMEDIAIRE, BENCHMARK_AVANCE


# ─────────────────────────────────────────────
# Coq → FR  (rétro-traduction)
# ─────────────────────────────────────────────
def traduire_coq_vers_fr(mistral: Mistral, code_coq: str) -> str:
    response = mistral.chat.complete(
        model="mistral-small-latest",
        messages=[
            {
                "role": "system",
                "content": (
                    "Tu es un mathématicien francophone expert en Coq. "
                    "Traduis le théorème Coq suivant en un énoncé mathématique "
                    "clair en français, sans code, sans syntaxe Coq. "
                    "Donne uniquement l'énoncé, rien d'autre."
                ),
            },
            {"role": "user", "content": f"```coq\n{code_coq}\n```"},
        ],
    )
    return response.choices[0].message.content.strip()


# ─────────────────────────────────────────────
# Comparaison sémantique
# ─────────────────────────────────────────────
def comparer_conjectures(mistral: Mistral, original: str, retraduit: str) -> tuple[bool, str]:
    response = mistral.chat.complete(
        model="mistral-small-latest",
        messages=[
            {
                "role": "system",
                "content": (
                    "Tu es un expert en logique mathématique. "
                    "Compare les deux énoncés et dis s'ils expriment "
                    "la même conjecture mathématique. "
                    "Réponds UNIQUEMENT par :\n"
                    "- EQUIVALENT si les deux énoncés ont le même sens mathématique.\n"
                    "- DIFFERENT suivi d'une explication courte des différences sinon."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Énoncé original :\n{original}\n\n"
                    f"Énoncé rétrotraduit :\n{retraduit}"
                ),
            },
        ],
    )
    verdict = response.choices[0].message.content.strip()
    return verdict.upper().startswith("EQUIVALENT"), verdict


# ─────────────────────────────────────────────
# Autocorrection pour UN énoncé
# ─────────────────────────────────────────────
def autocorrection(mistral: Mistral, texte_fr: str, max_cycles: int = 3) -> str:
    """
    Retourne :
      "✅ Prouvé et vérifié"     → Coq OK + FR rétrotraduit ≈ original
      "⚠️  Prouvé mais divergent" → Coq OK mais rétrotraduction différente après max_cycles
      "❌ Échec Coq"              → trad_enonce() n'a pas réussi
    """
    texte_fr_original = texte_fr
    prompt_courant    = texte_fr

    for cycle in range(1, max_cycles + 1):
        print(f"    [Cycle {cycle}/{max_cycles}] FR→Coq...")

        # ── Étape 1 : FR → Coq ──
        resultat = trad_enonce(texte_fr=prompt_courant)
        if resultat != "Prouvé !":
            return f"❌ Échec Coq : {resultat}"

        # ── Étape 2 : lecture de temp.v ──
        with open("temp.v", "r") as f:
            code_coq = f.read()

        # ── Étape 3 : Coq → FR ──
        fr_retraduit = traduire_coq_vers_fr(mistral, code_coq)
        print(f"    [Cycle {cycle}] Rétrotraduit : {fr_retraduit[:100]}...")

        # ── Étape 4 : Comparaison ──
        equivalent, explication = comparer_conjectures(
            mistral, texte_fr_original, fr_retraduit
        )

        if equivalent:
            return "✅ Prouvé et vérifié"

        # ── Étape 5 : feedback ──
        print(f"    [Cycle {cycle}] ⚠️  Divergence : {explication[:120]}")
        prompt_courant = (
            f"Le théorème Coq produit ne capture pas fidèlement l'énoncé original.\n\n"
            f"Énoncé original (français) :\n{texte_fr_original}\n\n"
            f"Ce que ton code Coq exprime (rétrotraduit) :\n{fr_retraduit}\n\n"
            f"Différences :\n{explication}\n\n"
            f"Reprends l'énoncé original et produis un théorème Coq fidèle."
        )

    return "⚠️  Prouvé mais divergent"


# ─────────────────────────────────────────────
# Benchmark
# ─────────────────────────────────────────────
def run_benchmark_autocorrection(enonces: list, nom: str, mistral: Mistral, max_cycles: int = 3):
    """Lance la boucle d'autocorrection sur une liste d'énoncés et affiche un résumé."""
    print(f"\n{'#'*60}")
    print(f"  BENCHMARK : {nom}  ({len(enonces)} énoncés)")
    print(f"{'#'*60}")

    resultats = []
    for i, enonce in enumerate(enonces, 1):
        print(f"\n[{i}/{len(enonces)}] {enonce}")
        statut = autocorrection(mistral, enonce, max_cycles=max_cycles)
        print(f"  => {statut}")
        resultats.append((enonce, statut))

    # Résumé
    prouves_verifies  = sum(1 for _, r in resultats if r == "✅ Prouvé et vérifié")
    prouves_divergent = sum(1 for _, r in resultats if r == "⚠️  Prouvé mais divergent")
    echecs            = sum(1 for _, r in resultats if r.startswith("❌"))

    print(f"\n{'─'*60}")
    print(f"  {nom} — Résultats :")
    print(f"    ✅ Prouvé et vérifié  : {prouves_verifies}/{len(enonces)}")
    print(f"    ⚠️  Prouvé mais divergent : {prouves_divergent}/{len(enonces)}")
    print(f"    ❌ Échec Coq          : {echecs}/{len(enonces)}")
    print(f"{'─'*60}")

    return resultats


# ─────────────────────────────────────────────
# Point d'entrée
# ─────────────────────────────────────────────
if __name__ == "__main__":
    key = os.getenv("MISTRAL_API_KEY")
    if not key:
        print("❌ Erreur : variable d'environnement MISTRAL_API_KEY manquante.")
        exit(1)

    with Mistral(api_key=key) as mistral:
        run_benchmark_autocorrection(BENCHMARK_FACILE,        "Facile",        mistral)
        run_benchmark_autocorrection(BENCHMARK_INTERMEDIAIRE, "Intermédiaire", mistral)
        run_benchmark_autocorrection(BENCHMARK_AVANCE,        "Avancé",        mistral)
