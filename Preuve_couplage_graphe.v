From Coq Require Import Arith Bool List Lia.
Import ListNotations.
Require Import ProofIrrelevance.

(*BUT JUSTE DEFINIR LOGIQUEMENT LES CONCEPTS*)

(* ############################################################ *)
(* 1. Graphes finis simples (non orientés, sans boucles)        *)
(* ############################################################ *)

Section FiniteGraph.

  (* n = nombre de sommets : on les indexe par 0..n-1 *)
  Variable n : nat.

  (* Un sommet est un nat < n. On encode ça par { i : nat | i < n }. *)
  Definition sommet : 
  Type := { i : nat | i < n }.

  (* test d’égalité sommet *)
  Definition sommet_eqb (u v : sommet) : bool :=
    Nat.eqb (proj1_sig u) (proj1_sig v).
   
   (* eqb= equality boolean permet de faire la comparaison, proj1_sig= permet d'extraire la valeur que contient ce type*
   Nat.eqb= compare deux entier naturel*)

 Axiom vertex_eqb_spec :
    forall u v, sommet_eqb u v = true <-> u = v.

  (* Un graphe simple = matrice d’adjacence booléenne avec
     - symétrie (non orienté)
     - pas de boucle (adj u u = false)
  *)
  Record Graph : Type := {
    adj : sommet -> sommet -> bool;

    adj_symmetric :
      forall u v, adj u v = adj v u;

    adj_irreflexive :
      forall u, adj u u = false
  }.

  Definition all_vertices : list sommet :=
    let fix build acc k {struct k} :=
        match k with
        | 0 => acc
        | S k' =>
            match lt_dec k' n with
            | left H =>  (* cas k' < n *)
                build (exist _ k' H :: acc) k'
            | right _ => (* cas k' >= n *)
                build acc k'
            end
        end in
    build [] n.
  (* on démarre avec liste vide *)


  (* ############################################################ *)
  (* 2. Chemins et connexité                                     *)
  (* ############################################################ *)

  (* Un chemin de u à v est une liste de sommets, telle que :
       - la liste commence à u
       - se termine à v
       - chaque arête successive est présente dans adj
  *)
  Inductive path (G : Graph) : sommet -> sommet -> list sommet -> Prop :=
  | path_single :
      forall v,
        path G v v [v]
  | path_cons :
      forall u v w rest,
        adj G u v = true ->
        path G v w rest ->
        path G u w (u :: rest).

  (* G est connexe si tout couple de sommets est relié par un chemin *)
  Definition connected (G : Graph) : Prop :=
    forall (u v : sommet), exists p : list sommet, path G u v p.

  (* ############################################################ *)
  (* 3. Griffe (claw) et graphes sans griffe                     *)
  (* ############################################################ *)

  (* Une griffe : sommet centre c, trois voisins a,b,d distincts,
     mutuellement non adjacents.
     NB : ici on ne parle pas d’induit, seulement du motif, pour simplifier.
  *)
  Definition est_griffe (G : Graph) : Prop :=
    exists (c a b d : sommet),
      a <> b /\ a <> d /\ b <> d /\
      adj G c a = true /\
      adj G c b = true /\
      adj G c d = true /\
      adj G a b = false /\
      adj G a d = false /\
      adj G b d = false.

  Definition griffe (G : Graph) : Prop :=
    ~ est_griffe G.

  (* ############################################################ *)
  (* 4. Couplages et couplages parfaits                          *)
  (* ############################################################ *)

  (* Une arête est un couple (u,v) avec u,v sommets *)
  Definition arrete : Type := (sommet * sommet)%type.

  (* vérifie que l’arête est valide :
     - extremités distinctes
     - adjacentes dans G
  *)
  Definition valide_griffe (G : Graph) (a : arrete) : Prop :=
    let '(u, v) := a in
    u <> v /\ adj G u v = true.

  (* prédicat : u est incident à e *)
  Definition incident (u : sommet) (e : arrete) : Prop :=
    let '(x,y) := e in x = u \/ y = u.

  (* Un couplage M est :
     - un ensemble d’arêtes valides
     - deux arêtes distinctes ne partagent pas de sommet (sommets disjoints)
  *)
  (* ############################################################ *)
  (* 4. Couplages et couplages parfaits                          *)
  (* ############################################################ *)

  (* Une arête est un couple (u,v) avec u,v sommets *)
  Definition Arête : Type := (sommet * sommet)%type.

  (* vérifie que l'arête est valide :
     - extremités distinctes
     - adjacentes dans G
  *)
  Definition arête_valide (G : Graph) (a : arrete) : Prop :=
    let '(u, v) := a in
    u <> v /\ adj G u v = true.


  (* Un couplage M est :
     - un ensemble d'arêtes valides
     - deux arêtes distinctes ne partagent pas de sommet
  *)
  Definition couplage (G : Graph) (M : list Arête) : Prop :=
    (* 1) chaque arête de M est valide *)
    (forall arete, In arete M -> arête_valide G arete) /\
    (* 2) les arêtes sont deux à deux disjointes en sommets *)
    (forall arete1 arete2 u,
        In arete1 M -> In arete2 M ->
        arete1 <> arete2 ->
        incident u arete1 ->
        ~ incident u arete2).

  (* Un sommet est couvert par le couplage M s'il est incident à une arête de M *)
  Definition couvert_par (M : list Arête) (u : sommet) : Prop :=
    exists arete, In arete M /\ incident u arete.

  (* Couplage parfait :
     - M est un couplage
     - chaque sommet est couvert exactement une fois
  *)
  Definition couplage_parfait (G : Graph) (M : list arrete) : Prop :=
    couplage G M /\
    forall u : sommet,
      exists! a : arrete, In a M /\ incident u a.

  (* ############################################################ *)
  (* 5. Ordre du graphe et parité                               *)
  (* ############################################################ *)

  Definition ordre (G : Graph) : nat := n.

  Definition ordre_pair (G : Graph) : Prop := Nat.even n = true.

  (* Graphe sans griffe *)
  Definition sans_griffe (G : Graph) : Prop := ~ est_griffe G.

  (* ############################################################ *)
  (* 6. Énoncé de Sumner–Las Vergnas                             *)
  (* ############################################################ *)

  Theorem Sumner_LasVergnas :
    forall (G : Graph),
      connected G ->
      sans_griffe G ->
      ordre_pair G ->
      exists M : list Arête, couplage_parfait G M.
  Proof.
  Admitted.

End FiniteGraph.


