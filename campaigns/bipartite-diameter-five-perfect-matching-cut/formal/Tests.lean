import Challenge
open BipartiteDiameterFivePerfectMatchingCut
-- One crossing edge at each vertex; the output cut need not be a graph coloring.
example : perfectCut ⟨4, [(0,1),(1,2),(2,3),(3,0)]⟩ [false,false,true,true] = true := by native_decide
example : perfectCut ⟨3, [(0,1),(1,2),(2,0)]⟩ [false,true,true] = false := by native_decide
example : legalSource ⟨3, [[0,1,1]]⟩ = false := by native_decide
example : sourceWitness ⟨3, [[0,1,2]]⟩ [true,false,false] = true := by native_decide
example : sourceWitness ⟨3, [[0,1,2]]⟩ [false,false,false] = false := by native_decide
example : legalTarget ⟨6, [(0,1),(1,2),(2,3),(3,4),(4,5)]⟩ = true := by native_decide
example : legalTarget ⟨7, [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6)]⟩ = false := by native_decide

example : 1024 ≤ (encodeGraph ⟨1024, []⟩).length := by native_decide
