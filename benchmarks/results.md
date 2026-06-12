# Benchmark Results — v0.3 (first run)

**Date:** 2026-06-11 · **Corpus:** 200 uniform workflow entries (goal → task → agent → result/retry), generated with `run.py` (seed 42) · **Tokenizers:** real vocabularies, cl100k_base (GPT-4) and o200k_base (GPT-4o) · **Legend cost:** 80 tokens, counted against SCP.

## Totals (o200k_base; cl100k within ±1%)

| Format | Tokens | Savings vs prose |
|---|---|---|
| English prose | 4,932 | — |
| Compact JSON (one object/line) | 4,326 | 12% |
| **TOON** | **2,307** | **53%** |
| SCP-C (no legend) | 2,428 | 51% |
| **SCP-C + legend** | **2,508** | **49%** |

## Break-even curve (tokens, o200k_base)

| Entries | Prose | JSON | TOON | SCP+legend |
|---|---|---|---|---|
| 5 | 136 | 107 | 70 | 139 |
| 8 | 207 | 172 | 105 | 177 |
| 10 | 258 | 216 | 128 | 200 |
| 20 | 507 | 431 | 241 | 322 |
| 50 | 1,218 | 1,079 | 582 | 681 |
| 200 | 4,932 | 4,326 | 2,307 | 2,508 |

SCP (legend included) beats prose from **~7 entries** and compact JSON from **~9 entries**. Full curve: `curve_o200k.csv`, `curve_cl100k.csv`.

## Hypothesis outcomes

- **H1 (≥40% vs prose, net):** ✅ confirmed — 49%.
- **H2 (≥30% vs JSON, net):** ✅ confirmed — 42%.
- **H3 (≥95% LLM interpretation fidelity):** ⏳ pending — requires LLM grading runs.

## Honest finding: TOON wins on this corpus

TOON beat SCP by ~4 points (53% vs 49%). This corpus is **uniform tabular data — TOON's declared sweet spot**: its header declares fields once, so rows carry no markers, while every SCP line repeats `G/T:/A:`. We publish this rather than hide it.

SCP's hypothesized advantage is **heterogeneous state**: variable-length chains, optional metadata, mixed entry types (memory entries, rules, groups), where TOON degrades to nested YAML-like form. That scenario is **not yet measured** — it is the next benchmark before any claim is made.

## Reproduce

```bash
pip install tiktoken
python benchmarks/run.py --vocab path/to/o200k_base.tiktoken --name o200k_base --csv curve.csv
```
