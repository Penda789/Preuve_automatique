import json
import ollama
import asyncio
from BibliLemme import verify_proof_in_coq # Ta fonction de communication

# 1. CHARGEMENT DE LA BIBLIOTHÈQUE
def load_library():
    with open("graph_library.json", "r") as f: #pour l'instant elle est vide, ouvre fichier json cree dans biblilemme
        return json.load(f)

# 2. LE SÉLECTEUR (Choisit les outils pour l'IA)
def select_relevant_lemmas(theorem_goal, library, n=10):
    # on cherche les mots clés communs entre le but et les lemmes, dcp on les decoupe et tt cpour ca ya split 
    keywords = theorem_goal.lower().split()
    scored_lemmas = []
    for name, statement in library.items():
        score = sum(1 for word in keywords if word in statement.lower() or word in name.lower()) # comme son nom l'indique on note les lemmes en f(x) de si ils correspondent bien à l'obj
        scored_lemmas.append((score, name, statement))
    
    # On trie et on prend les 10 meilleurs
    scored_lemmas.sort(reverse=True)
    return scored_lemmas[:n]

# 3. LA BOUCLE DE MUTATION/FEEDBACK
async def funsearch_loop(goal, max_iterations=5):
    library = load_library()
    relevant_lemmas = select_relevant_lemmas(goal, library)
    
    # c une liste de lemmes ( dcp qu'on a choisi dans la f(x) de tt à l'heure) que l'IA va lire
    context_str = "\n".join([f"- {name}: {stmt}" for _, name, stmt in relevant_lemmas])
    
    current_error = "" # erreur que coq a return
    
    for i in range(max_iterations):
        print(f"\n🔄 Itération {i+1}/{max_iterations}")
        
        # PROMPT : On donne le but, les lemmes et l'erreur précédente, en gros comme moi qd je parle à chatgpt je reprends ce qui est bon et lui dire de faire attention à ce qui ne l'est pas --> AUTOMATISATION
        prompt = f"""
        Tu es un expert Coq. Prouve ce théorème : {goal}
        Utilise ces lemmes si besoin :
        {context_str}
        
        {f"Ta tentative précédente a échoué avec cette erreur : {current_error}. Corrige-la." if current_error else ""}
        
        Réponds UNIQUEMENT avec le code Coq entre ```coq ... ```.
        """
        
        # APPEL OLLAMA
        response = ollama.chat(model='deepseek-coder-v2:lite', messages=[
            {'role': 'user', 'content': prompt},
        ])
        
        proof_attempt = response['message']['content']
        print("🤖 L'IA propose une preuve...")

        # ÉVALUATION DANS COQ
        success, error_msg = await verify_proof_in_coq(proof_attempt)

        if success:
            print("PREUVE TROUVÉE !")
            print(proof_attempt)
            return proof_attempt
        else:
            print(f"Échec. Erreur Coq : {error_msg}")
            current_error = error_msg # On injecte l'erreur dans l'itération suivante

    print("Max iterations atteint sans succès.")
    return None

if __name__ == "__main__":
    goal_to_prove = "Theorem handshaking : forall G : graph, sum_degrees G = 2 * num_edges G."
    asyncio.run(funsearch_loop(goal_to_prove))