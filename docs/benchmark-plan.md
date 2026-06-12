# Benchmark Plan — v0.3

The central claim of SCP is net token savings on structured agent state. This plan defines how to validate it credibly.

## Hypotheses

- H1: SCP-C uses ≥40% fewer tokens than English prose for the same operational state, net of legend cost, at ≥15 entries.
- H2: SCP-C uses ≥30% fewer tokens than compact JSON for the same state.
- H3: LLMs reconstruct the original meaning from SCP-C + legend with ≥95% fidelity.

## Method

1. **Corpus:** 200 workflow entries sampled from realistic multi-agent scenarios (content pipeline, support triage, data ETL), each in four representations: English prose, compact JSON, TOON, SCP-C.
2. **Token counting:** tiktoken `o200k_base` and at least one open tokenizer (Llama). Report tokens per entry and total including a 120-token legend amortized over the document.
3. **Fidelity test (H3):** give an LLM the SCP-C document + legend, ask it to expand each entry to natural language; a second model grades semantic equivalence against the source prose (blind, rubric-based).
4. **Break-even curve:** plot net savings vs number of entries (1–100) to publish the exact break-even point instead of the current ~15-entry estimate.

## Baselines

English prose, compact JSON (no whitespace), TOON (closest competitor — see [related-work.md](related-work.md)), and abbreviated English ("goal>task>agent done").

## Deliverables

`benchmarks/results.md` with tables and charts, raw CSVs, and the runner script `benchmarks/run.py`. Results — favorable or not — go in the README. If TOON wins on any axis, document it; credibility is worth more than a claim.
