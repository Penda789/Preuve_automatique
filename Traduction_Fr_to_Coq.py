#!/usr/bin/env python3
# pour pas que ça s'execute comme un script bash 

import subprocess
import os
from mistralai.client import Mistral
import re

def trad_enonce():
    #cle api "0Lrp5o1vP2xjfXv7hh7s5zkAdd3PWNxM"
    #pTekYKZfndlGAm2mHt8USDw5rh50YBei

    tentative = 0
    max_tentatives=4
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
                    {"role": "user", "content": f"Traduis cet énoncé en langage Coq : {texte_fr}, ne me donne pas d'indication. Contente toi uniquement de produire en coq"}
                ]
            )

            code_coq=response.choices[0].message.content
            # Vérification que la réponse n'est pas vide
            if not code_coq:
                erreur = "Réponse vide de l'API Mistral"
                texte_fr = f"Erreur: {erreur}\nRéessaie de traduire: {texte_fr}"
                continue  # passe à la tentative suivante

            """#pour qu'il y ai que du COQ sinon met la rep de mistral aussi dedans et dcp compilation echoue
            match = re.search(r"```coq\n(.*?)```", code_coq, re.DOTALL)
            if match:
                code_coq = match.group(1)"""
            
            # Écriture fichier temp
            with open("temp.v", "w") as f:
                f.write(code_coq)
            
            # Compilation Coq
            result = subprocess.run(["coqc", "temp.v"], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                return "Prouvé !"
            else:
                erreur = result.stderr
                texte_fr = f"Erreur Coq: {erreur}\nCorrige ce code Coq: {code_coq}"
        
    return f"Échec après {max_tentatives} tentatives"

if __name__ == "__main__":
    enonce = "Prouve que pour tout n nombre naturel, n + 0 = n."
    trad_enonce()

