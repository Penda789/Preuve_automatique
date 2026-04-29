#!/usr/bin/env python3
# pour pas que ça s'execute comme un script bash 

import subprocess
import os
from mistralai.client import Mistral
import re
from PythonToCoq import toCoq

def trad_enonce(texte_fr=None):
    #cle api "0Lrp5o1vP2xjfXv7hh7s5zkAdd3PWNxM"
    #pTekYKZfndlGAm2mHt8USDw5rh50YBei

    tentative = 0
    max_tentatives=4
    if texte_fr is None:
        texte_fr=input("Entrez l'ennoncé à prouver:")

    key = os.getenv("MISTRAL_API_KEY")  
    if not key:
        return "Erreur: clé API manquante"
    
    with Mistral(api_key=key) as mistral:
        code_coq = None
        
        while tentative < max_tentatives:
            tentative += 1
            # Génération code Coq
            response = mistral.chat.complete(
                model="mistral-small-latest",
                messages=[
                    {"role":"system", "content":"Tu es un expert en Coq. Traduis l'énoncé en théorème Coq  {texte_fr} et prouve-le. Règles strictes :1. N'utilise QUE la bibliothèque standard de Coq. N'importe jamais mathcomp, ssreflect, Omega, ou Z. 2. Pour les graphes, utilise des types simples (ex: `Variable V : Type. Variable E : V -> V -> Prop.`).3. Ne fais aucune supposition sur des lemmes externes non standards.4. Réponds UNIQUEMENT avec le bloc de coq """}
                ]
            )

            code_coq=response.choices[0].message.content
            # Vérification que la réponse n'est pas vide
            if not code_coq:
                erreur = "Réponse vide de l'API Mistral"
                texte_fr = f"Erreur: {erreur}\nRéessaie de traduire: {texte_fr}"
                continue  # passe à la tentative suivante

            #pour qu'il y ai que du COQ sinon met la rep de mistral aussi dedans et dcp compilation echoue
            match = re.search(r"```coq\n(.*?)```", code_coq, re.DOTALL)
            if match:
                code_coq = match.group(1)
            
            # Écriture fichier temp
            with open("temp.v", "w") as f:
                f.write(code_coq)
            
            # Compilation Coq
            success, message = toCoq()
            if success:
                return "Prouvé !"
            else:
                erreur = message
                texte_fr = f"Erreur Coq: {erreur}\nCorrige ce code Coq: {code_coq}"
        
    return f"Échec après {max_tentatives} tentatives, voici l'erreur produite {erreur}"

from benchmark_graphes import (
    BENCHMARK_FACILE,
    BENCHMARK_INTERMEDIAIRE,
    BENCHMARK_AVANCE,
)

def run_benchmark(enonces, nom="benchmark"):
    resultats = []
    for i, enonce in enumerate(enonces, 1):
        print(f"\n[{i}/{len(enonces)}] {enonce}")
        res = trad_enonce(texte_fr=enonce)
        print(f"  => {res}")
        resultats.append((enonce, res))
    succes = sum(1 for _, r in resultats if r == "Prouvé !")
    print(f"\n=== {nom} : {succes}/{len(enonces)} réussis ===")
    return resultats

if __name__ == "__main__":
    run_benchmark(BENCHMARK_FACILE, "Facile")
    run_benchmark(BENCHMARK_INTERMEDIAIRE, "Intermediaire")
    run_benchmark(BENCHMARK_AVANCE,        "Avance")
