"""Fix seeded Positive NAE-3-SAT cases before construction."""

import json
import random
from itertools import combinations
from pathlib import Path


FIVE_TRIPLES = [list(values) for values in combinations(range(5),3)]


def formula(n,clauses):
    return {"num_vars":n,"clauses":clauses}


EDGE_CASES = [
    (formula(0,[]),True), (formula(1,[]),True), (formula(2,[]),True),
    (formula(3,[[0,1,2]]),True),
    (formula(3,[[0,1,2],[0,1,2]]),True),
    (formula(4,[list(values) for values in combinations(range(4),3)]),True),
    (formula(4,[[0,1,2],[0,1,3],[0,2,3]]),True),
    (formula(5,FIVE_TRIPLES),False),
    (formula(5,FIVE_TRIPLES+[[0,1,2]]),False),
    (formula(6,FIVE_TRIPLES),False),
    (formula(5,[]),True),
    (formula(6,[[0,1,2],[3,4,5]]),True),
    (formula(5,[clause for clause in FIVE_TRIPLES if clause != [0,1,2]]),True),
]


def random_source(seed):
    rng = random.Random(seed)
    n = rng.randint(5,8)
    if seed % 2 == 0:
        hidden = [rng.randrange(2) == 1 for _ in range(n)]
        if all(hidden) or not any(hidden):
            hidden[0] = not hidden[0]
        choices = [list(values) for values in combinations(range(n),3)
                   if 0 < sum(hidden[v] for v in values) < 3]
        rng.shuffle(choices)
        clauses = choices[:rng.randint(1,min(12,len(choices)))]
    else:
        clauses = list(FIVE_TRIPLES)
        choices = [list(values) for values in combinations(range(n),3)
                   if list(values) not in clauses]
        rng.shuffle(choices)
        clauses += choices[:rng.randint(0,min(8,len(choices)))]
    return formula(n,clauses)


def build_cases():
    from check import solve_source
    cases, seen = [], set()

    def add(source,kind,seed=None,hand_answer=None):
        key = json.dumps(source,sort_keys=True,separators=(",", ":"))
        if key in seen:
            return False
        seen.add(key)
        answer = solve_source(source)
        if hand_answer is not None and ("assignment" in answer) != hand_answer:
            raise AssertionError(f"Hand label disagrees with oracle: {source}")
        case = {"source":source,"kind":kind,"expected":answer}
        if seed is not None:
            case["seed"] = seed
        cases.append(case)
        return True

    for source,expected in EDGE_CASES:
        add(source,"edge",hand_answer=expected)
    seed = 0
    while sum(case["kind"] == "random" for case in cases) < 100:
        add(random_source(seed),"random",seed=seed)
        seed += 1
    return cases


if __name__ == "__main__":
    path = Path(__file__).with_name("cases.json")
    cases = build_cases()
    path.write_text(json.dumps(cases,indent=2)+"\n")
    print(f"Wrote {len(cases)} cases to {path}")
