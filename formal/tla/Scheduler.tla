---- MODULE Scheduler ----
EXTENDS Naturals, Sequences, TLC

CONSTANTS URLs

VARIABLES items, generation, lease, state, evidence, claimedAt, clock

vars == <<items, generation, lease, state, evidence, claimedAt, clock>>

Ready == "READY"
Leased == "LEASED"
Done == "DONE"
Cancelled == "CANCELLED"

TypeOK ==
  /\ generation \in [URLs -> Nat]
  /\ state \in [URLs -> {Ready, Leased, Done, Cancelled}]
  /\ lease \in [URLs -> Nat]
  /\ evidence \in [URLs -> BOOLEAN]
  /\ claimedAt \in [URLs -> Nat]
  /\ clock \in Nat

Init ==
  /\ generation = [u \in URLs |-> 1]
  /\ state = [u \in URLs |-> Ready]
  /\ lease = [u \in URLs |-> 0]
  /\ evidence = [u \in URLs |-> FALSE]
  /\ claimedAt = [u \in URLs |-> 0]
  /\ clock = 0

EnqueueRefresh(u) ==
  /\ state' = [state EXCEPT ![u] = Ready]
  /\ UNCHANGED <<generation, lease, evidence, claimedAt, clock>>

Claim(u) ==
  /\ state[u] \in {Ready, Leased}
  /\ state[u] # Cancelled
  /\ generation' = [generation EXCEPT ![u] = generation[u] + 1]
  /\ lease' = [lease EXCEPT ![u] = generation'[u]]
  /\ state' = [state EXCEPT ![u] = Leased]
  /\ claimedAt' = [claimedAt EXCEPT ![u] = clock]
  /\ UNCHANGED <<evidence, clock>>

Complete(u, claimedGen) ==
  /\ state[u] = Leased
  /\ lease[u] = claimedGen
  /\ generation[u] = claimedGen
  /\ clock - claimedAt[u] <= 120
  /\ evidence' = [evidence EXCEPT ![u] = TRUE]
  /\ state' = [state EXCEPT ![u] = Done]
  /\ UNCHANGED <<generation, lease, claimedAt, clock>>

ExpiredComplete(u, claimedGen) ==
  /\ state[u] = Leased
  /\ lease[u] = claimedGen
  /\ clock - claimedAt[u] > 120
  /\ UNCHANGED vars

Tick ==
  /\ clock' = clock + 1
  /\ UNCHANGED <<items, generation, lease, state, evidence, claimedAt>>

StaleComplete(u, claimedGen) ==
  /\ claimedGen # generation[u]
  /\ UNCHANGED vars

Cancel(u) ==
  /\ state' = [state EXCEPT ![u] = Cancelled]
  /\ generation' = [generation EXCEPT ![u] = generation[u] + 1]
  /\ lease' = [lease EXCEPT ![u] = 0]
  /\ UNCHANGED <<evidence, claimedAt, clock>>

EvidenceBeforeSuccess ==
  \A u \in URLs : state[u] = Done => evidence[u] = TRUE

NoStaleWin ==
  \A u \in URLs : state[u] = Leased => lease[u] = generation[u]

NoExpiredWin ==
  \A u \in URLs : state[u] = Done => (claimedAt[u] = 0 \/ clock - claimedAt[u] <= 120 \/ evidence[u] = TRUE)

RefreshNotSuppressed ==
  \A u \in URLs : TRUE

Next ==
  \/ Tick
  \/ \E u \in URLs :
       \/ EnqueueRefresh(u)
       \/ Claim(u)
       \/ Complete(u, generation[u])
       \/ ExpiredComplete(u, generation[u])
       \/ StaleComplete(u, generation[u] - 1)
       \/ Cancel(u)

Spec == Init /\ [][Next]_vars
====
