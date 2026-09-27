# Research instructions

Read the [fixed question](campaigns/bipartite-diameter-five-perfect-matching-cut/question.md), [prior state](campaigns/bipartite-diameter-five-perfect-matching-cut/state.md) and [preparation notes](campaigns/bipartite-diameter-five-perfect-matching-cut/work/preparation.md). The fixed [test corpus](campaigns/bipartite-diameter-five-perfect-matching-cut/work/cases.json) and [verifier](campaigns/bipartite-diameter-five-perfect-matching-cut/work/check.py) are the starting evidence; the preparation notes state their coverage and any pending checks.

Run `uv sync --locked`, then `uv run --locked python campaigns/bipartite-diameter-five-perfect-matching-cut/work/check.py --self-test` before relying on that evidence. Follow the current user's AutoResearch pipeline. Scope and budgets in the state describe earlier work and do not limit a new campaign. Preserve prior evidence, commit new work incrementally and make only evidence-backed claims.
