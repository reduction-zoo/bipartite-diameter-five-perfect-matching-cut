from check import legal_source, solve_source, valid_source, legal_target, solve_target, valid_target


def test_hand_cases():
    clause = {"num_vars":3,"clauses":[[0,1,2]]}
    assert valid_source(clause,{"assignment":[True,False,False]})
    assert not valid_source(clause,{"assignment":[True,True,True]})
    complete5 = {"num_vars":5,"clauses":[[a,b,c] for a in range(5) for b in range(a+1,5) for c in range(b+1,5)]}
    assert solve_source(complete5) == {"status":"NO-SOLUTION"}
    assert not legal_source({"num_vars":3,"clauses":[[0,0,1]]})
    edge = {"vertices":2,"edges":[[0,1]]}
    assert valid_target(edge,{"side":[False,True]})
    triangle = {"vertices":3,"edges":[[0,1],[1,2],[0,2]]}
    assert not legal_target(triangle)
    path6 = {"vertices":6,"edges":[[i,i+1] for i in range(5)]}
    assert "side" in solve_target(path6)


if __name__ == "__main__":
    test_hand_cases()
