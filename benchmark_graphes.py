#!/usr/bin/env python3
# =============================================================
# benchmark_graphes.py
# Trois niveaux de benchmark en theorie des graphes (francais)
# a passer dans Traduction_Fr_to_Coq.py
# =============================================================

# --------------------------------------------------------------
# NIVEAU 1 - FACILE (7 enonces)
# Proprietes de base : irreflexivite, symetrie, degre,
# ensembles triviaux.  Formulations volontairement courtes pour
# maximiser la compilation directe par Mistral.
# --------------------------------------------------------------
BENCHMARK_FACILE = [
    "Prouve que pour tout graphe simple, aucun sommet n'est adjacent a lui-meme.",
    "Prouve que dans un graphe non oriente, si u est adjacent a v alors v est adjacent a u.",
    "Prouve que l'ensemble vide est un ensemble independant dans tout graphe.",
    "Prouve que tout singleton contenant un seul sommet est un ensemble independant dans un graphe sans boucle.",
    "Prouve que le degre de tout sommet dans un graphe a n sommets est inferieur ou egal a n.",
    "Prouve que le couplage vide est un couplage valide dans tout graphe.",
    "Prouve que l'ensemble de tous les sommets d'un graphe est une couverture par sommets.",
]

# --------------------------------------------------------------
# NIVEAU 2 - INTERMEDIAIRE (12 enonces)
# Chemins, connexite, ensembles independants, couplages, arbres.
# Formulations un peu plus riches mais toujours non ambigues.
# --------------------------------------------------------------
BENCHMARK_INTERMEDIAIRE = [
    "Prouve que si deux sommets u et v sont adjacents dans un graphe G, il existe un chemin de longueur 1 entre u et v.",
    "Prouve que si u est adjacent a v et v est adjacent a w dans un graphe G, il existe un chemin de longueur 2 entre u et w.",
    "Prouve que tout chemin reduit a un seul sommet est un chemin valide.",
    "Prouve que dans un graphe, la relation etre connecte par un chemin est reflexive.",
    "Prouve que dans un graphe non oriente, la relation etre connecte par un chemin est symetrique.",
    "Prouve que si S est un ensemble independant et S2 est un sous-ensemble de S, alors S2 est aussi un ensemble independant.",
    "Prouve que dans un graphe G, la taille d'un ensemble independant est inferieure ou egale au nombre de sommets.",
    "Prouve que si deux sommets u et v sont adjacents dans G, alors aucun ensemble independant ne contient a la fois u et v.",
    "Prouve que dans tout couplage M d'un graphe G a n sommets, la taille de M est inferieure ou egale a n divise par 2.",
    "Prouve que si M est un couplage et e est une arete dont les extremites n'appartiennent a aucune arete de M, alors l'union de M et de e est aussi un couplage.",
    "Prouve que la taille d'un couplage est inferieure ou egale a la taille de toute couverture par sommets.",
    "Prouve qu'un graphe a un seul sommet sans arete est un arbre.",
]

# --------------------------------------------------------------
# NIVEAU 3 - AVANCE (13 enonces)
# Theoremes classiques : handshaking, König, coloration,
# bipartite, arbres.  Ces enonces peuvent necessiter plusieurs
# tentatives ou echouer : c'est l'objectif du benchmark.
# --------------------------------------------------------------
BENCHMARK_AVANCE = [
    "Prouve que le complementaire d'un ensemble independant maximal est une couverture par sommets.",
    "Prouve que tout arbre a n sommets possede exactement n moins 1 aretes.",
    "Prouve que dans un arbre il existe un unique chemin entre toute paire de sommets.",
    "Prouve que tout arbre est un graphe biparti.",
    "Prouve que tout graphe sans aretes est 1-colorable.",
    "Prouve que le graphe K2 compose de deux sommets relies par une arete est 2-colorable.",
    "Prouve que le graphe K2 n'est pas 1-colorable.",
    "Prouve que tout graphe biparti est 2-colorable.",
    "Prouve que si un graphe G est k-colorable alors tout sous-graphe de G est k-colorable.",
    "Prouve que dans tout graphe fini la somme des degres de tous les sommets est egale au double du nombre d'aretes.",
    "Prouve que dans tout graphe fini le nombre de sommets de degre impair est pair.",
    "Prouve que tout graphe connexe a n sommets possede au moins n moins 1 aretes.",
    "Prouve que dans un graphe biparti la taille du couplage maximum est egale a la taille de la couverture minimum par sommets.",
]

# =============================================================
#  INTEGRATION DANS Traduction_Fr_to_Coq.py
# =============================================================
#
#  ETAPE 1 — Modifier la signature de trad_enonce()
#  -------------------------------------------------
#  Change :
#
#      def trad_enonce():
#          texte_fr = input("Entrez l'ennonce a prouver:")
#
#  en :
#
#      def trad_enonce(texte_fr=None):
#          tentative = 0
#          max_tentatives = 4
#          if texte_fr is None:          # mode interactif conserve
#              texte_fr = input("Entrez l'ennonce a prouver:")
#          # ...reste du code inchange...
#
#  ETAPE 2 — Ajouter run_benchmark() dans Traduction_Fr_to_Coq.py
#  ---------------------------------------------------------------
#  Colle ces lignes apres la definition de trad_enonce() :
#
#      from benchmark_graphes import (
#          BENCHMARK_FACILE,
#          BENCHMARK_INTERMEDIAIRE,
#          BENCHMARK_AVANCE,
#      )
#
#      def run_benchmark(enonces, nom="benchmark"):
#          resultats = []
#          for i, enonce in enumerate(enonces, 1):
#              print(f"\n[{i}/{len(enonces)}] {enonce}")
#              res = trad_enonce(texte_fr=enonce)
#              print(f"  => {res}")
#              resultats.append((enonce, res))
#          succes = sum(1 for _, r in resultats if r == "Prouve !")
#          print(f"\n=== {nom} : {succes}/{len(enonces)} reussis ===")
#          return resultats
#
#  ETAPE 3 — Remplacer le bloc if __name__ == "__main__":
#  -------------------------------------------------------
#      if __name__ == "__main__":
#          # Un seul niveau :
#          run_benchmark(BENCHMARK_FACILE,        "Facile")
#          # run_benchmark(BENCHMARK_INTERMEDIAIRE, "Intermediaire")
#          # run_benchmark(BENCHMARK_AVANCE,        "Avance")
#
#          # Ou les 3 niveaux a la suite :
#          # run_benchmark(
#          #     BENCHMARK_FACILE + BENCHMARK_INTERMEDIAIRE + BENCHMARK_AVANCE,
#          #     "Complet"
#          # )
#
# =============================================================

if __name__ == "__main__":
    niveaux = [
        ("FACILE",        BENCHMARK_FACILE),
        ("INTERMEDIAIRE", BENCHMARK_INTERMEDIAIRE),
        ("AVANCE",        BENCHMARK_AVANCE),
    ]
    total = 0
    for nom, enonces in niveaux:
        print(f"\n--- {nom} ({len(enonces)} enonces) ---")
        for i, e in enumerate(enonces, 1):
            print(f"  [{i:02d}] {e}")
        total += len(enonces)
    print(f"\nTotal : {total} enonces")
