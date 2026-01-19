import pycoq.serapi

# On essaie d'ouvrir une session Coq
try:
    # La config par défaut utilise SerAPI
    with pycoq.serapi.CoqSerapi.get() as coq:
        print("Succès ! Coq est piloté par Python.")
        # On demande à Coq de calculer 2+2
        response = coq.execute("Compute 2 + 2.")
        print(f"Réponse de Coq : {response}")
except Exception as e:
    print(f"Erreur : {e}")