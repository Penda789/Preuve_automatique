import pycoq.serapi as serapi
from pycoq.common import LocalKernelConfig as lkc
from pycoq.kernel import LocalKernel as Lc
import asyncio, re

# !! ADAPTE ce chemin avec le résultat de ta commande find
GRAPH_THEORY_PATH = "/home/psow/.opam/pycoq_env/lib/coq/user-contrib/GraphTheory"

async def extraction():
    kernel = None
    try:
        lemmes = []

        coq_cfg = lkc(
            command=[
                "/home/psow/.opam/pycoq_env/bin/sertop",
                f"--load-path={GRAPH_THEORY_PATH},GraphTheory"
            ],
            pwd="/home/psow"
        )

        kernel = Lc(coq_cfg)
        await kernel.start()
        s = serapi.CoqSerapi(kernel)

        # execute() renvoie (sid_debut, sid_fin, [CoqExn], [msgs])
        sid_start, sid_end, exns, msgs = await s.execute('From GraphTheory Require Import digraph.')
        print(f"digraph -> sid={sid_end}, exns={exns}")

        sid_start, sid_end, exns, msgs = await s.execute('From GraphTheory Require Import ugraph.')
        sid_start, sid_end, exns, msgs = await s.execute('Require Import Vertex.')
        sid_start, sid_end, exns, msgs = await s.execute('Require Import Edge.')
        sid_start, sid_end, exns, msgs = await s.execute('From GraphTheory Require Import edone.')

        # Search . -- les résultats reviennent dans msgs (4e élément)
        sid_start, sid_end, exns, msgs = await s.execute('Search _.')
        print(f"Search -> exns={exns}, msgs preview={str(msgs)[:300]}")

        # Parse les résultats
        for msg in msgs:
            txt = str(msg)
            for line in txt.splitlines():
                m = re.match(r"^([A-Za-z0-9_'.]+)\s*:", line)
                if m:
                    lemmes.append(line.strip())

        print(f"\n{len(lemmes)} lemmes trouvés.")
        for j in lemmes[:10]:  # affiche les 10 premiers
            print("  ", j)

        return lemmes

    finally:
        if kernel is not None:
            for method_name in ['stop', 'shutdown', 'terminate', 'kill']:
                method = getattr(kernel, method_name, None)
                if callable(method):
                    try:
                        r = method()
                        if asyncio.iscoroutine(r):
                            await r
                        break
                    except Exception:
                        continue

if __name__ == "__main__":
    asyncio.run(extraction())
