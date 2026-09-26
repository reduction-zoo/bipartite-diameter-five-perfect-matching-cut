# Positive NAE-3-SAT → Bipartite diameter-five Perfect Matching Cut

Category: Complexity open

## Source

A source instance is a conjunction of clauses of three distinct unnegated variables. A valid assignment gives both truth values to every clause; an infeasible instance returns NO-SOLUTION.

## Target

The target is a connected bipartite graph of diameter at most five. A witness is a nontrivial vertex bipartition in which every vertex has exactly one neighbor across the cut; otherwise the output is NO-SOLUTION.

## Required result

Construct deterministic polynomial-time maps F and G: F sends every legal source instance to a legal target instance, and G(x,y) is a valid source output for every valid output y of F(x). Preserve the stated threshold, domain and promises. The requested complexity conclusion is NP-hardness for the stated target problem.

## Acceptance

Give explicit construction and recovery algorithms, a general proof for every legal input and every valid target output, and polynomial runtime and encoding-size bounds. Specify finite output encodings and handle NO-SOLUTION outputs when applicable. Tests compare recovered source outputs with independent source solutions.

## Why it matters

The diameter restriction targets a missing boundary in the structural complexity of perfect matching cuts.

## Difficulty

Shortening distances must preserve the exact one-crossing-neighbor constraint at every vertex.

## Literature context

The cited classification leaves the bipartite diameter-five case between established tractable and hard cases.

Literature checked 2026-09-15. This summarizes the archived literature search on the date above. Unpublished, unindexed and overlooked work remains outside coverage; no new novelty assessment was performed.

## References

- [arXiv:2501.08735](https://arxiv.org/html/2501.08735): All six gates pass provisionally. Gate 1: fixed languages and both maps above. Gates 2–3: Lucke, https://arxiv.org/html/2501.08735, Section 5 Open Problem 3, asks bipartite PMC for diameters four through nine; its diameter-three algorithm does not cover five. The preceding local radius-three result implies diameter at most six, not five. Searches on 2026-09-15 included "Perfect Matching Cut" "bipartite" "diameter 5" and "Perfect Matching Cut" "diameter" "2026" bipartite. No exact later resolution was located. Historical hyphenated perfect matching-cut may mean DPM and is not interchangeable. Unindexed/overlooked work is not excluded.

Fixed from board record `website/questions/bipartite-diameter-five-perfect-matching-cut.json` in board checkout at 6c7d3bd9c0a8f595279969a9c0a4d1853a3f5c17; the record was copied from the current working tree.
