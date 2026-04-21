#!/usr/bin/env python3 
"""d'ailleurs ça s'appele un shebang, pour dire à l'os on utilise quel interpreteur"""
"""BUT: Executer le code automatiquement en COQ via ce script"""
import subprocess

def toCoq():
    #intialisation
    import os

    proc = subprocess.Popen(
        [
            "sudo","docker", "run", "--rm", 
            "-v", f"{os.getcwd()}:/workspace",  # Monte le dossier actuel dans le conteneur
            "-w", "/workspace",                  # Définit /workspace comme dossier de travail
            "mon_image_coq",           # <--- REMPLACE CECI par le nom de l'image (ex: coqorg/coq)
            "sercomp", "--printer=human", "temp.v"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    #execution
    stdout,stderr= proc.communicate(timeout=30)

    #recherche si jamais ya une erreur
    if "CoqExn" in stdout or proc.returncode != 0:
        return False, stdout + stderr

    return True, ""

success, message = toCoq()
if success:
    print("✅ Proof verified!")
else:
    print("❌ Coq error:\n", message)
