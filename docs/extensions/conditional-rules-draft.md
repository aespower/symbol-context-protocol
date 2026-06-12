# SCP Extension Draft — Conditional Rules (SCP-R)

**Status:** experimental draft. Not part of core until validated by the v0.3 benchmark.

## Motivation

Agents carry decision policies in every context window ("if execution failed and the task is high priority, retry it"). These rules are structured and repetitive — exactly SCP's niche. Measured savings: **~45% per rule vs English prose**, with a one-line legend cost (~15 tokens), so the extension pays for itself from the second rule onward.

This extension is strictly **declarative**: SCP-R defines how to *write* a condition, never how to *evaluate* it. Evaluation belongs to the host system (the LLM or orchestrator reading the context). This keeps SCP a protocol, not a runtime — no scores are computed, no weights are updated by SCP itself.

## Syntax

```ebnf
rule      = "?" , group , ">" , chain ;          (* condition → consequence *)
weight    = "W:" , identifier , "=" , number ;   (* weight recorded as data *)
```

| SCP-C | SCP-V | Meaning |
|---|---|---|
| `?[...]` | ❓[...] | Condition: if all signals in the group are present/true |
| `W:name=0.8` | ⚖️(name: 0.8) | A weight stored as data (host system reads/updates it) |

## Examples

```txt
?[FAIL+HIGH]>RTY              If failed and high priority → retry          (~6 tok vs ~14 prose)
?[G+VID+REV]>A:video          If goal involves video and revenue → activate video agent
?[M:short_pref]>T:short_video If memory says user prefers short videos → prioritize them
W:short_video=0.8             Recorded signal strength (data, not computation)
```

A policy block for an agent context:

```txt
# RULES
?[FAIL+HIGH]>RTY
?[FAIL+LOW]=OK(skip)
?[G+VID+REV]>A:video
W:short_video=0.8
```

## Explicitly out of scope

- Computing priorities or scores (no thresholds with magic numbers like `th:0.70` — where would the number come from?).
- Updating weights automatically ("learning"). The host may rewrite `W:` lines; SCP only gives them a compact representation.
- Any "neuron" semantics. SCP-R is rule notation, nothing more.

These exclusions are deliberate: adding evaluation would turn the protocol into a framework, contradict "SCP is not a programming language" (see concept.md), and the metadata-heavy syntax would erode the token savings that justify SCP in the first place.

## Adoption criteria

SCP-R graduates from draft to core when the v0.3 benchmark confirms: (1) ≥30% net savings on a realistic 20+ rule policy corpus vs prose, and (2) ≥95% LLM interpretation fidelity with only the one-line legend. Parser support (`?` and `W:` in scp.py) lands with v0.3.
