import json
import re
import asyncio
from pycoq.common import LocalKernelConfig as lkc
from pycoq.kernel import LocalKernel as Lc
# On importe ta fonction d'extraction ou on adapte la logique
import PythonToCoq as ptc

def parse_coq_output(raw_lines):
    """
    Transforme les lignes de Coq en un dictionnaire.
    """
    library = {}
    # Regex pour capturer "Nom : Enoncé"
    # On cherche un mot suivi de ':' et on prend tout ce qui suit jusqu'au point.
    pattern = re.compile(r"^([A-Za-z0-9_']+)\s*:\s*(.*)")

    for line in raw_lines:
        match = pattern.match(line)
        if match:
            name = match.group(1)
            statement = match.group(2)
            library[name] = statement
    return library

async def verify_proof_in_coq(proof_script):
    """
    Prend une preuve (string), l'exécute dans Coq et renvoie (Succès, Message).
    """
    kernel = None
    try:
        # Configuration identique à ton script d'extraction
        coq_cfg = lkc(
            command=["/home/psow/.opam/pycoq_env/bin/sertop"],
            pwd="/home/psow"
        )
        kernel = Lc(coq_cfg)
        await kernel.start()
        s = serapi.CoqSerapi(kernel)

        # On charge l'environnement de graphes
        await s.execute('Require Import digraph ugraph edone' \
        ' Vertex Edge.')

        # On nettoie le script de l'IA (on enlève les balises ```coq)
        clean_script = proof_script.replace("```coq", "").replace("```", "").strip()
        
        # On exécute la preuve
        # Note : On envoie tout d'un coup ou ligne par ligne
        # Ici on essaie d'exécuter le bloc. Si Coq renvoie une erreur, Python lève une Exception.
        await s.execute(clean_script)
        
        # Si on arrive ici sans exception, on vérifie si la preuve est fermée
        # On tente un Qed. pour être sûr.
        await s.execute('Qed.')
        
        return True, "Preuve validée par Coq."

    except Exception as e:
        # On capture l'erreur précise pour que l'IA puisse corriger
        return False, str(e)
    
    finally:
        if kernel is not None:
            await kernel.shutdown()

# --- Garde tes fonctions existantes en dessous ---
def parse_coq_output(raw_lines):
    library = {}
    pattern = re.compile(r"^([A-Za-z0-9_']+)\s*:\s*(.*)")
    for line in raw_lines:
        match = pattern.match(line)
        if match:
            library[match.group(1)] = match.group(2)
    return library

async def save_library():
    print("Démarrage de l'extraction des lemmes.")
    
    # Ici, on suppose que tu as modifié BibliLemme pour retourner la liste 'lemmes'
    # Pour l'exemple, j'utilise une liste fictive si tu n'as pas encore fait le return
    raw_lemmes = await ptc.extraction() 
    
    if not raw_lemmes:
        print("Aucun lemme trouvé. Vérifie tes imports Coq.")
        return

    # Nettoyage
    clean_library = parse_coq_output(raw_lemmes)
    
    # Sauvegarde en JSON
    with open("graph_library.json", "w") as f:
        json.dump(clean_library, f, indent=4, ensure_ascii=False)
    
    print(f"Bibliothèque créée : {len(clean_library)} lemmes sauvegardés dans graph_library.json")

if __name__ == "__main__":
    asyncio.run(save_library())



""" les bibliotheque qu'il y a acgtk                                           --          Abst
acpc                                            --          Chem
aliases                                         --          In m
altgr-ergo                                      --          The
archimedes                                      --          Exte
async_graphics                                  --          Asyn
bap-callgraph-collator                          --          Coll
bap-dependencies                                --          Anal
bap-emacs-dot                                   --          Will
bap-emacs-goodies                               --          A co
binbin                                          --          Conv
blake2                                          --          Blak
blake3                                          --          Blak
bls12-381                                       --          Impl
bls12-381-hash                                  --          Impl
bogue                                           --          GUI
bytesrw                                         --          Comp
cairo2                                          --          Bind
camlimages                                      --          Imag
claudius                                        --          A re
codept                                          --          Alte
cohttp-bench                                    --          Benc
conex                                           --          Esta
conf-graphviz                                   --          Virt
coq-addition-chains                             --          Expo
coq-color                                       --          A li
coq-corn                                        --          The
coq-ctltctl                                     --          Comp
coq-dijkstra                                    --          A Ve
coq-dpdgraph                                    --          Comp
coq-equations                                   --          A fu
coq-euclidean-geometry                          --          Basi
coq-fiat-crypto                                 --          Cryp
coq-fourcolor                                   --          Mech
coq-games                                       --          A li
coq-graph-basics                                --          a Co
coq-graph-theory                                --          Gene
coq-graph-theory-planar                         --          Grap
coq-graph2tac                                   --          Grap
coq-graphs                                      --          Sati
coq-higman-cf                                   --          A di
coq-higman-nw                                   --          A pr
coq-higman-s                                    --          Higm
coq-hydra-battles                               --          Expl
coq-izf                                         --          Intu
coq-kruskal-veldman                             --          Wim
coq-mathcomp-ssreflect                          --          Smal
coq-mathcomp-tarjan                             --          Stro
coq-mk-choice-axiom-and-equivalent-propositions --          Mach
coq-ollibs                                      --          OL l
coq-otway-rees                                  --          Otwa
coq-railroad-crossing                           --          The
coq-ramsey                                      --          Rams
coq-rewriter                                    --          Refl
coq-ssprove                                     --          A Fo
coq-tactician                                   --          Tact
coq-tortoise-hare-algorithm                     --          Tort
coq-tree-diameter                               --          Diam
coqide                                          --          The
cryptohash                                      --          hash
cryptokit                                       --          A li
cryptoverif                                     --          Cryp
dblp                                            --          Comm
dblp-api                                        --          Libr
depgraph                                        --          dot
dirsp-proscript                                 --          OCam
dirsp-proscript-mirage                          --          Mira
dream                                           --          Tidy
dune-deps                                       --          Show
dune_deps_extra                                 --          Addi
ego                                             --          Ego
fasmifra                                        --          Mole
febusy                                          --          Embe
fiat-p256                                       --          Prim
fmlib                                           --          Func
fungi                                           --          A pu
gd                                              --          OCam
genspir                                         --          Gene
gg                                              --          Basi
gl-legacy                                       --          Lega
glMLite                                         --          Open
gnuplot                                         --          Simp
gr                                              --          OCam
graphics                                        --          The
graphicspdf                                     --          Vers
graphlib                                        --          Gene
graphql                                         --          Buil
graphql-async                                   --          Buil
graphql-cohttp                                  --          Run
graphql-lwt                                     --          Buil
graphql_jsoo_client                             --          Grpa
graphql_parser                                  --          Libr
graphql_ppx                                     --          Grap
graphv                                          --          Top_
graphv_core                                     --          Func
graphv_core_lib                                 --          Prim
graphv_font                                     --          Func
graphv_font_js                                  --          Java
graphv_font_stb_truetype                        --          STB
graphv_gles2                                    --          Func
graphv_gles2_native                             --          Full
graphv_gles2_native_impl                        --          Nati
graphv_webgl                                    --          Full
graphv_webgl_impl                               --          WebG
gremlin                                         --          Grem
gxl-light                                       --          Gxl
hacl_x25519                                     --          Prim
hugin                                           --          Visu
imguiml                                         --          ImGU
incremental_cycles                              --          A st
inspect                                         --          Insp
irmin-graphql                                   --          Grap
irmin-mirage-graphql                            --          Mira
jasmin                                          --          Comp
kaun                                            --          Flax
kittyimg                                        --          An i
llvmgraph                                       --          Ocam
macaroons                                       --          Maca
maxminddb                                       --          Bind
memgraph                                        --          A sm
memgraph_kitty                                  --          Disp
memtrace_viewer                                 --          Inte
mesh-display                                    --          Tria
mesh-graphics                                   --          Tria
mirage-crypto                                   --          Simp
mirage-crypto-ec                                --          Elli
mirage-crypto-pk                                --          Simp
mirage-crypto-rng                               --          A cr
mirage-crypto-rng-lwt                           --          A cr
mirage-crypto-rng-mirage                        --          Entr
mlpost                                          --          OCam
mlpost-lablgtk                                  --          Libr
module-graph                                    --          The
molenc                                          --          Mole
nocrypto                                        --          Simp
noise                                           --          The
notty_async                                     --          An A
ocamldot                                        --          Pars
ocamlgraph                                      --          A ge
ocamlgraph_gtk                                  --          Disp
ocamlsdl2                                       --          Inte
ocamlsdl2-image                                 --          Inte
ocamlsdl2-ttf                                   --          Inte
octez-bls12-381-hash                            --          Impl
octez-mec                                       --          Modu
odep                                            --          Depe
odnnr                                           --          Regr
odoc-depgraph                                   --          Cust
oneffs                                          --          One-
opam-graph                                      --          Grap
opium-graphql                                   --          Run
oplsr                                           --          OCam
oqamldebug                                      --          Grap
orf                                             --          OCam
otfm                                            --          Open
otp                                             --          Time
owl-base                                        --          An O
owl-top                                         --          An O
pkcs11                                          --          PKCS
pkcs11-driver                                   --          Bind
plotly                                          --          Bind
producer                                        --          Accu
proj4                                           --          Bind
prometheus                                      --          Clie
prometheus-app                                  --          Clie
proverif                                        --          ProV
proverifdoc                                     --          Docu
random                                          --          Easy
randoml                                         --          Gene
rdf                                             --          OCam
rdr                                             --          Rdr
regl                                            --          OCam
rocq-color                                      --          A li
rocq-equations                                  --          A fu
rocq-mathcomp-boot                              --          Smal
rocq-mathcomp-ssreflect                         --          Smal
rocq-ollibs                                     --          OL l
rocqide                                         --          The
satyrographos                                   --          A pa
sfml                                            --          Bind
sha                                             --          Bind
splittable_random                               --          PRNG
statverif                                       --          Stat
stog                                            --          A st
stog-rdf                                        --          Plug
stog-writing                                    --          Stog
stog_dot                                        --          Stog
stog_writing                                    --          Stog
subscriptions-transport-ws                      --          Webs
tezos-crypto                                    --          Tezo
tezos-crypto-dal                                --          DAL
tgls                                            --          Thin
tls                                             --          Tran
tls-eio                                         --          Tran
tree_layout                                     --          Algo
tsdl                                            --          Thin
tsdl-image                                      --          SDL2
tsdl-ttf                                        --          SDL2
ttweetnacl                                      --          Thin
ulid                                            --          ULID
unison-gui                                      --          File
uuseg                                           --          Unic
vg                                              --          Decl
volgo                                           --          A Ve
volgo-git-backend                               --          An I
volgo-git-eio                                   --          A Gi
volgo-git-unix                                  --          A Gi
volgo-hg-backend                                --          An I
volgo-hg-eio                                    --          A Me
volgo-hg-unix                                   --          A Me
vpt                                             --          Vant
wall                                            --          Real
wayland                                         --          Pure
webauthn                                        --          WebA
wxOCaml                                         --          OCam
x509                                            --          Publ
xoshiro  """