# Prepared input and output contract

The Positive NAE-3-SAT source input is `{"num_vars": n, "clauses":
[[v1,v2,v3], ...]}` with `n >= 0` and each clause containing three distinct
unnegated variable indices in `0..n-1`. Repeated clauses are allowed. A
source output is `{"assignment": [bool, ...]}` assigning both truth
values within each clause, or `{"status": "NO-SOLUTION"}` exactly when
no such assignment exists. An empty clause list is satisfiable.

The target input is `{"vertices": n, "edges": [[u,v], ...]}` with a
connected simple undirected bipartite graph, `n >= 1`, of diameter at most
five. A target output is `{"side": [bool, ...]}`, a nontrivial bipartition
for which every vertex has exactly one neighbor on the opposite side.
The alternative `{"status": "NO-SOLUTION"}` is valid exactly when no
such cut exists. The graph's bipartition is a legal-instance promise;
the output cut need not equal that bipartition.

A candidate `algorithm.py` reads one source JSON object from stdin and
writes a legal target JSON object to stdout. With `--extract`, it reads
`{"source": source, "target_solution": output}` and writes a valid source
output. The commands share no memory, exit nonzero on errors, and send
diagnostics to stderr. They must be deterministic and polynomial time;
recovery must work for every valid target cut or negative answer.

`check.py --candidate PATH` independently solves constructed targets on
the fixed source corpus and directly validates recovered source answers.
