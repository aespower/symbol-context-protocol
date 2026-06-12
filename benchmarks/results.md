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

---

# Heterogeneous Benchmark (second run, same date)

**Corpus:** 200 mixed entries — 80 plain workflows, 40 workflows with metadata (priority, deadline), 30 memory entries, 30 conditional rules (SCP-R), 20 group goals — shuffled to simulate a real agent log. Script: `run_het.py` (seed 42). Legend (with SCP-R extension): 94 tokens, counted against SCP.

## Results (o200k_base; cl100k within ±2%)

| Format | Tokens | vs prose | Preserves entry order? |
|---|---|---|---|
| English prose | 3,638 | — | ✅ |
| Compact JSON | 5,065 | **−39% (worse)** | ✅ |
| TOON, grouped by type | 2,417 | 34% | ❌ destroyed |
| TOON, order-preserving (nested) | 5,809 | **−60% (worse)** | ✅ |
| **SCP-C + legend** | **2,710** | **26%** | ✅ |

## Findings

1. **SCP is the only format that both saves tokens and preserves order on heterogeneous state.** Order-preserving TOON costs 2.1x more than SCP; compact JSON is worse than prose here.
2. **TOON grouped still wins raw token count (+8 pts)** — but at two real costs: global entry order is destroyed (fatal for execution logs and event streams), and variable-arity values must be smuggled into cells as ad-hoc `|`-strings, which is no longer self-describing TOON.
3. **Niche definition, now data-backed:** use TOON for bulk uniform data dumps where order is irrelevant; use SCP-C for ordered, heterogeneous, append-friendly agent state (logs, memory, rules, mixed workflows). The formats are complementary.
4. SCP's savings dropped vs the uniform corpus (26% vs 49%) mainly because metadata syntax `(priority:high,deadline:d12)` is token-expensive — an optimization target for v0.4.

## Reproduce

```bash
python benchmarks/run_het.py --vocab path/to/o200k_base.tiktoken --name o200k_base
```
