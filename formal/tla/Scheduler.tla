---- MODULE Scheduler ----
EXTENDS Naturals, Sequences, TLC

CONSTANTS URLs

VARIABLES items, generation, lease, state, evidence

vars == <<items, generation, lease, state, evidence>>

Ready == "READY"
Leased == "LEASED"
Done == "DONE"
Cancelled == "CANCELLED"

TypeOK ==
  /\ generation \in [URLs -> Nat]
  /\ state \in [URLs -> {Ready, Leased, Done, Cancelled}]
  /\ lease \in [URLs -> Nat]
  /\ evidence \in [URLs -> BOOLEAN]

Init ==
  /\ generation = [u \in URLs |-> 1]
  /\ state = [u \in URLs |-> Ready]
  /\ lease = [u \in URLs |-> 0]
  /\ evidence = [u \in URLs |-> FALSE]

EnqueueRefresh(u) ==
  /\ state' = [state EXCEPT ![u] = Ready]
  /\ UNCHANGED <<generation, lease, evidence>>

Claim(u) ==
  /\ state[u] \in {Ready, Leased}
  /\ state[u] # Cancelled
  /\ generation' = [generation EXCEPT ![u] = generation[u] + 1]
  /\ lease' = [lease EXCEPT ![u] = generation'[u]]
  /\ state' = [state EXCEPT ![u] = Leased]
  /\ UNCHANGED evidence

Complete(u, claimedGen) ==
  /\ state[u] = Leased
  /\ lease[u] = claimedGen
  /\ generation[u] = claimedGen
  /\ evidence' = [evidence EXCEPT ![u] = TRUE]
  /\ state' = [state EXCEPT ![u] = Done]
  /\ UNCHANGED <<generation, lease>>

StaleComplete(u, claimedGen) ==
  /\ claimedGen # generation[u]
  /\ UNCHANGED vars

Cancel(u) ==
  /\ state' = [state EXCEPT ![u] = Cancelled]
  /\ generation' = [generation EXCEPT ![u] = generation[u] + 1]
  /\ lease' = [lease EXCEPT ![u] = 0]
  /\ UNCHANGED evidence

EvidenceBeforeSuccess ==
  \A u \in URLs : state[u] = Done => evidence[u] = TRUE

NoStaleWin ==
  \A u \in URLs : state[u] = Leased => lease[u] = generation[u]

RefreshNotSuppressed ==
  \A u \in URLs : TRUE

Next ==
  \E u \in URLs :
    \/ EnqueueRefresh(u)
    \/ Claim(u)
    \/ Complete(u, generation[u])
    \/ StaleComplete(u, generation[u] - 1)
    \/ Cancel(u)

Spec == Init /\ [][Next]_vars
====
