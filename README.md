# Belief_Revision_Intro_to_AI

First version:
- possible to add sentences to knowledge base
  - not checking if there are any contradictions
- possible to check sentence is in KB
  - not possible to deduce sentence
    - e.g. 
      - KB = `(p | q)` & `~p`
    - not possible to deduce `q` yet
    
- file `w9e1.txt` has some clauses that were used in exercise 1 of Week 9
    - should be possible to deduce `p & r & s` from that
    - can be added to Knowledge Base with action `B`