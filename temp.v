```coq
From Coq Require Import Arith.

Lemma plus_n_0 : forall n : nat, n + 0 = n.
Proof.
  intros n.
  induction n as [| n' IHn'].
  - (* Cas de base : n = 0 *)
    reflexivity.
  - (* Cas inductif : n = S n' *)
    simpl.
    rewrite IHn'.
    reflexivity.
Qed.
```