# Preparation evidence

Prepared on 2026-09-26 before construction. The fixed corpus has 113
distinct legal Positive NAE-3-SAT formulas: 13 hand-labelled edge cases
and 100 seeded random cases, with 68 YES and 45 NO decisions and zero to
eight variables. `generate_cases.py` retains the seeds and generator;
`cases.json` stores checked assignments or NO-SOLUTION. Positive cases
are seeded from a NAE assignment. Negative cases include every triple
among five variables, which cannot be two-colored without a monochromatic
triple. Z3 4.16.0 requires one true and one false literal in each clause.
Every model is checked by direct clause evaluation, and exhaustive Boolean
assignments agreed on all 113 formulas. UNSAT is conclusive; unknown is an
error.

Target legality is checked by direct breadth-first bipartiteness,
connectivity and diameter tests. Z3 constrains a nontrivial Boolean side
assignment and exactly one opposite neighbor per vertex. Returned cuts
are checked again by direct neighbor counting. Independent exhaustive
side assignments agreed with Z3 on 65 distinct connected bipartite target
graphs with at most eight vertices. Hand fixtures cover a valid edge cut,
an invalid triangle, a valid six-vertex path at diameter five, and invalid
source clauses.

Reproduce from the repository root:

```sh
uv sync --locked
uv run --locked python campaigns/bipartite-diameter-five-perfect-matching-cut/work/check.py --self-test
```

The self-test starts with the corpus gate, regenerates seeded source
formulas, rechecks labels and witnesses, and compares target decisions
with exhaustive enumeration. The candidate runner uses separate forward
and recovery subprocesses and up to three target cuts per source. An
incorrect injected candidate was rejected after target solving and
source validation. No actual reduction candidate exists; finite checks
do not establish hardness or a general reduction.
