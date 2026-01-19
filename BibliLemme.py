import pycoq.serapi as serapi
from pycoq.common import LocalKernelConfig as lkc
from pycoq.kernel import LocalKernel as Lc
import asyncio, re


async def extraction():
    kernel = None
    try:
        lemmes = []

        with open("context.v", "w") as f:
            f.write("")

        coq_cfg = lkc(
            command=["/home/psow/.opam/pycoq_env/bin/sertop"],
            pwd="/home/psow"
        )

        kernel = Lc(coq_cfg)
        await kernel.start()

        s = serapi.CoqSerapi(kernel)

        await s.execute('Require Import DG.')
        await s.execute('Require Import UG.')
        await s.execute('Require Import CDG.')
        await s.execute('Require Import CUG.')
        await s.execute('Require Import Vertex.')
        await s.execute('Require Import Edge.')

        # Pour Search, on doit récupérer les feedbacks/réponses du kernel
        # execute() retourne juste un sid (int), pas les messages
        await s.execute('Redirect "context.v" Search _.')
         # on s'assure que Coq a fini
        await s.execute('(* done *)')

        with open("context.v", "r") as f:
            for ligne in f:
                    ligne = ligne.strip()
                    m=re.match(r"^([A-Za-z0-9_']+)\s*:", ligne)
                    if m:
                        lemmes.append(ligne)
        for j in lemmes:
            print("Les lemmes",j)

    finally:
        if kernel is not None:
            # Essayer différentes méthodes de fermeture
            for method_name in ['stop', 'shutdown', 'terminate', 'kill']:
                method = getattr(kernel, method_name, None)
                if callable(method):
                    try:
                        result = method()
                        if asyncio.iscoroutine(result):
                            await result
                        break
                    except Exception:
                        continue


if __name__ == "__main__":
    asyncio.run(extraction())
