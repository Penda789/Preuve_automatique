"""import pycoq.serapi as serapi # c'est ce qui me permet de faire le lien avec coq, de faire des commandes
from pycoq.common import LocalKernelConfig as lkc
from pycoq.kernel import LocalKernel as Lc # kernel c comme un terminal coq, dcp besoin d'un local p
import asyncio

asyncio.get_event_loop_policy().get_event_loop()


async def extraction(): # await a besoin de async pour fonctinner
    lemmes=[]
    with open("context.v","w") as f:
        f.write("") #cree un fichier .v a chaque fois 

    coq = lkc(
    command=["/home/psow/.opam/pycoq_env/bin/sertop"],
    pwd="/home/psow"
    )

    kernel = Lc(coq)
    await kernel.start()

    s=serapi.CoqSerapi(kernel) #Serapi() c la classe

    await s.execute('Require Import DG.')
    await s.execute('Require Import UG.')
    await s.execute('Require Import CDG.')
    await s.execute('Require Import CUG.')
    await s.execute('Require Import Verxtex.')
    await s.execute('Require Import Edge.')

    l = await s.execute('Search _.') #besoin du await prcq python fait une "coroutine" ( en gros comme si il le compile mais ne l'execute pas )
    for i in l.get("contents,[]"):
        if i.get("tag")=="CoqNotice":
            notice_text=i.get("contents","")
            lemmes.append(notice_text)
    
    for j in lemmes:
        print(j)

    await kernel.stop()

loop = asyncio.new_event_loop() # code de chatGPT prcq j'ain un "RuntimeError: Event loop is closed"
loop.run_until_complete(extraction())"""
import pycoq.serapi as serapi
from pycoq.common import LocalKernelConfig as lkc
from pycoq.kernel import LocalKernel as Lc
import asyncio

async def extraction():
    lemmes = []
    
    # Configuration du Kernel Coq
    coq = lkc(
        command=["/home/psow/.opam/pycoq_env/bin/sertop"],
        pwd="/home/psow"
    )

    kernel = Lc(coq)
    await kernel.start()
    s = serapi.CoqSerapi(kernel)

    # Importations
    await s.execute('Require Import DG. Require Import UG. Require Import CDG. Require Import CUG. Require Import Verxtex. Require Import Edge.')

    # L'exécution de Search renvoie souvent une liste de dictionnaires
    responses = await s.execute('Search _.') 

    # On boucle sur la liste des réponses reçues
    for response in responses:
        # On vérifie si response est un dictionnaire avant d'utiliser .get()
        if isinstance(response, dict):
            if response.get("tag") == "CoqNotice":
                notice_text = response.get("contents", "")
                lemmes.append(notice_text)
    
    for j in lemmes:
        print(j)

    await kernel.stop()

# Gestion propre de la boucle d'événement
if __name__ == "__main__":
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(extraction())
    finally:
        loop.close()
