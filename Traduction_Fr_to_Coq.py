#!/usr/bin/env python3
# pour pas que ça s'execute comme un script bash 

import subprocess
import os
from mistralai.client import Mistral

def trad_enonce(texte_fr, max_tentatives=3):
    

    tentative = 0

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
                    {"role": "user", "content": f"Traduis cet énoncé en Coq avec preuve automatique: {texte_fr}"}
                ]
            )
            code_coq = response.choices[0].message.content
            
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
        
    return "Échec après {max_tentatives} tentatives"

if __name__ == "__main__":
    enonce = "Prouve que pour tout n nombre naturel, n + 0 = n."
    print(trad_enonce(enonce))

