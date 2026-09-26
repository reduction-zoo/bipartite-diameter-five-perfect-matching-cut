"""Independent Positive NAE-3-SAT and bipartite Perfect Matching Cut oracles."""

import argparse
import json
import random
import subprocess
import sys
from collections import deque
from itertools import product
from pathlib import Path

import z3


def legal_source(source):
    if not isinstance(source,dict):
        return False
    n,clauses = source.get("num_vars"),source.get("clauses")
    return (type(n) is int and n >= 0 and isinstance(clauses,list)
            and all(isinstance(clause,list) and len(clause) == 3
                    and all(type(v) is int and 0 <= v < n for v in clause)
                    and len(set(clause)) == 3 for clause in clauses))


def direct_assignment(source,assignment):
    return (isinstance(assignment,list) and len(assignment) == source["num_vars"]
            and all(type(value) is bool for value in assignment)
            and all(any(assignment[v] for v in clause)
                    and not all(assignment[v] for v in clause)
                    for clause in source["clauses"]))


def solve_source(source):
    if not legal_source(source):
        raise ValueError("Illegal Positive NAE-3-SAT formula")
    variables = [z3.Bool(f"x_{i}") for i in range(source["num_vars"])]
    solver = z3.Solver()
    for clause in source["clauses"]:
        solver.add(z3.Or(*[variables[v] for v in clause]))
        solver.add(z3.Or(*[z3.Not(variables[v]) for v in clause]))
    result = solver.check()
    if result == z3.unsat:
        return {"status":"NO-SOLUTION"}
    if result != z3.sat:
        raise RuntimeError(f"Inconclusive source solver: {result}")
    model = solver.model()
    assignment = [z3.is_true(model.eval(v,model_completion=True)) for v in variables]
    if not direct_assignment(source,assignment):
        raise AssertionError("Z3 NAE assignment violates direct predicate")
    return {"assignment":assignment}


def valid_source(source,output):
    if not legal_source(source) or not isinstance(output,dict):
        return False
    if output == {"status":"NO-SOLUTION"}:
        return solve_source(source) == output
    return set(output) == {"assignment"} and direct_assignment(source,output["assignment"])


def adjacency(target):
    neighbors = [set() for _ in range(target["vertices"])]
    for u,v in target["edges"]:
        neighbors[u].add(v)
        neighbors[v].add(u)
    return neighbors


def legal_target(target):
    if not isinstance(target,dict):
        return False
    n,edges = target.get("vertices"),target.get("edges")
    if type(n) is not int or n < 1 or not isinstance(edges,list):
        return False
    seen = set()
    for edge in edges:
        if (not isinstance(edge,list) or len(edge) != 2
                or any(type(v) is not int or not 0 <= v < n for v in edge)
                or edge[0] == edge[1]):
            return False
        key = tuple(sorted(edge))
        if key in seen:
            return False
        seen.add(key)
    neighbors = adjacency(target)
    colors = {0:False}
    queue = deque([0])
    while queue:
        u = queue.popleft()
        for v in neighbors[u]:
            if v in colors:
                if colors[v] == colors[u]:
                    return False
            else:
                colors[v] = not colors[u]
                queue.append(v)
    if len(colors) != n:
        return False
    for start in range(n):
        distances = {start:0}
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in neighbors[u]:
                if v not in distances:
                    distances[v] = distances[u]+1
                    queue.append(v)
        if max(distances.values()) > 5:
            return False
    return True


def direct_cut(target,side):
    n = target["vertices"]
    return (isinstance(side,list) and len(side) == n
            and all(type(value) is bool for value in side)
            and any(side) and not all(side)
            and all(sum(side[u] != side[v] for v in neighbors) == 1
                    for u,neighbors in enumerate(adjacency(target))))


def target_solutions(target,limit=3):
    if not legal_target(target):
        raise ValueError("Illegal connected bipartite diameter-five graph")
    n = target["vertices"]
    side = [z3.Bool(f"side_{v}") for v in range(n)]
    solver = z3.Solver()
    solver.add(z3.Or(*side),z3.Or(*[z3.Not(value) for value in side]))
    for u,neighbors in enumerate(adjacency(target)):
        solver.add(z3.Sum(*[z3.If(side[u] != side[v],1,0) for v in neighbors]) == 1)
    outputs = []
    while len(outputs) < limit:
        result = solver.check()
        if result == z3.unsat:
            break
        if result != z3.sat:
            raise RuntimeError(f"Inconclusive target solver: {result}")
        model = solver.model()
        bits = [z3.is_true(model.eval(value)) for value in side]
        if not direct_cut(target,bits):
            raise AssertionError("Z3 matching cut violates direct predicate")
        outputs.append({"side":bits})
        solver.add(z3.Or(*[value != bit for value,bit in zip(side,bits)]))
    return outputs or [{"status":"NO-SOLUTION"}]


def solve_target(target):
    return target_solutions(target,1)[0]


def valid_target(target,output):
    if not legal_target(target) or not isinstance(output,dict):
        return False
    if output == {"status":"NO-SOLUTION"}:
        return solve_target(target) == output
    return set(output) == {"side"} and direct_cut(target,output["side"])


def exhaustive_target(target):
    for bits in product((False,True),repeat=target["vertices"]):
        if direct_cut(target,list(bits)):
            return {"side":list(bits)}
    return {"status":"NO-SOLUTION"}


def self_test():
    from generate_cases import EDGE_CASES,random_source
    from test_oracle import test_hand_cases

    root = Path(__file__).resolve().parents[3]
    path = Path(__file__).with_name("cases.json")
    subprocess.run([sys.executable,str(root/"research/validate_preparation.py"),str(path)],check=True,cwd=root)
    cases = json.loads(path.read_text())
    for source,expected in EDGE_CASES:
        assert ("assignment" in solve_source(source)) == expected
    for case in cases:
        source = case["source"]
        if case["kind"] == "random":
            assert random_source(case["seed"]) == source
        current = solve_source(source)
        exists = any(direct_assignment(source,list(bits))
                     for bits in product((False,True),repeat=source["num_vars"]))
        assert ("assignment" in current) == ("assignment" in case["expected"]) == exists
        assert valid_source(source,current) and valid_source(source,case["expected"])
    test_hand_cases()
    checked,seen = 0,set()
    for seed in range(200):
        rng = random.Random(seed)
        a,b = rng.randint(1,4),rng.randint(1,4)
        edges = [[0,a+v] for v in range(b)] + [[u,a] for u in range(1,a)]
        edges += [[u,a+v] for u in range(1,a) for v in range(1,b) if rng.randrange(2)]
        target = {"vertices":a+b,"edges":sorted(edges)}
        key = json.dumps(target,sort_keys=True)
        if key not in seen and legal_target(target):
            seen.add(key)
            assert ("side" in solve_target(target)) == ("side" in exhaustive_target(target))
            checked += 1
    print(f"Self-test passed: {len(cases)} independently labelled source cases and {checked} exhaustive bipartite target graphs")


def candidate_check(path):
    self_test()
    cases = json.loads(Path(__file__).with_name("cases.json").read_text())
    recovered = 0
    for case in cases:
        source = case["source"]
        forward = subprocess.run([sys.executable,str(path)],input=json.dumps(source),text=True,capture_output=True,check=True)
        target = json.loads(forward.stdout)
        if not legal_target(target):
            raise AssertionError(f"Illegal bipartite target: {target}")
        for output in target_solutions(target):
            if not valid_target(target,output):
                raise AssertionError(f"Invalid target oracle output: {output}")
            payload = {"source":source,"target_solution":output}
            extraction = subprocess.run([sys.executable,str(path),"--extract"],input=json.dumps(payload),text=True,capture_output=True,check=True)
            recovered_output = json.loads(extraction.stdout)
            if not valid_source(source,recovered_output):
                raise AssertionError(f"Invalid recovery from {output}: {recovered_output}")
            recovered += 1
    print(f"Candidate check passed: {len(cases)} source cases, {recovered} target outputs")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test",action="store_true")
    group.add_argument("--candidate",type=Path)
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        candidate_check(args.candidate)
