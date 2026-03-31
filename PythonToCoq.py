#!/usr/bin/env python3 
"""d'ailleurs ça s'appele un shebang, pour dire à l'os on utilise quel interpreteur"""
"""BUT: Executer le code automatiquement en COQ via ce script"""
import subprocess

def toCoq():
    #intialisation
    proc=subprocess.Popen( #creation d'un sous processus qui s'occupe de COQ
        ["sercomp","--printer=human", "temp.v"],
        stdout=subprocess.PIPE, #lis dans le processus 
        stderr=subprocess.PIPE, # pour les erreurs
        text=True # pour avoir des str et pas des bites
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
