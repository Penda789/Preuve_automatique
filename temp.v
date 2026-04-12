Require Import Arith.
Require Import List.
Require Import ZArith.
Require Import RelationClasses.
Require Import Setoid.
Require Import Morphisms.
Require Import Relation_Definitions.

Section Reflexivity_Path_Connected.
  Variable V : Type.
  Variable E : V -> V -> Prop.

  Inductive path : V -> V -> Prop :=
  | path_refl : forall x, path x x
  | path_step : forall x y z, E x y -> path y z -> path x z.

  Definition path_connected (x y : V) := exists p : path x y, True.

  Lemma path_connected_refl : forall x, path_connected x x.
  Proof.
    intros x.
    exists (path_refl x).
    constructor.
  Qed.
End Reflexivity_Path_Connected.
