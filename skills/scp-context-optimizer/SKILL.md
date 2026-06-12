---
name: scp-context-optimizer
description: Compress agent operational context (goals, tasks, agents, execution states, persistent memory) into SCP-C — the token-efficient ASCII layer of the Symbol Context Protocol — and render it as SCP-V (emoji) for humans. Use this skill whenever the user mentions SCP, Symbol Context Protocol, saving tokens in multi-agent systems, compressing context/memory/state/logs sent to an LLM, encoding workflow state compactly, or asks to translate between SCP notation, JSON, and human-readable form — even if they just say "optimiza este contexto" or "comprime el estado de los agentes".
---

# SCP Context Optimizer

Symbol Context Protocol (SCP) v0.2 represents agent operational state in two equivalent layers:

- **SCP-C (canonical):** dense ASCII, ~1 token per element. This is what travels through model context and gets stored in memory.
- **SCP-V (visual):** emoji rendering for humans only. Never send SCP-V to an LLM — emojis cost 2–4 tokens each.

Spec: https://github.com/aespower/symbol-context-protocol

## When to compress (and when not to)

SCP pays off on **structured, repetitive operational state**: workflow logs, task queues, agent memory, execution history. The dictionary legend costs ~120 tokens once per context, and each compressed entry saves ~10–20 tokens versus prose. So:

- **≥15 entries:** compress — net savings around 50%.
- **<15 entries or free-form text (essays, emails, reasoning):** do NOT compress. SCP is not for arbitrary prose, and the legend overhead would exceed the savings.

## Dictionary (v0.2)

| SCP-C | SCP-V | Meaning |
|---|---|---|
| `G` | 🎯 | Goal |
| `M` | 🧠 | Memory |
| `T` | 📋 | Task |
| `A` | 🤖 | Agent |
| `X` | ⚡ | Execute |
| `OK` | ✓ | Complete |
| `FAIL` | ✗ | Failed |
| `RTY` | 🔄 | Retry |
| `GROW` | 📈 | Growth |
| `REV` | 💰 | Revenue |
| `VID` | 🎬 | Video |

Codes must be single tokens in common tokenizers. When extending the dictionary, prefer short common English words/abbreviations over rare strings or digits (rare strings split into multiple tokens; digits collide with numeric values).

## Grammar

| SCP-C | SCP-V | Meaning |
|---|---|---|
| `>` | ↓ | sequence — leads to / assigned to |
| `=` | → | result — produces final outcome |
| `+` | + | combination |
| `:name` | (name) | parameter / label |
| `[ ]` | [ ] | group |
| `( )` | ( ) | metadata, e.g. `(priority:high)` |

`>` chains workflow steps; `=` marks only the final result. Symbols may take an index (`G1`, `T3`) to reference specific instances.

## Workflow

1. **Compressing prose → SCP-C:** identify the entities (goal, task, agent, execution, state) in each statement and emit one line per workflow entry, e.g. `G1>T:outline>A:editor=FAIL>RTY`. Drop narrative filler; keep names and outcomes. If a concept has no dictionary code, add it to a "Extended codes" legend at the top using a single-token English word, e.g. `IMG=image`.
2. **Sending to an LLM:** prepend the legend once (dictionary + grammar in ~10 lines), then the SCP-C block. Never include emojis.
3. **Showing humans:** render SCP-V with the script below, or expand to natural language if asked.
4. **Round-trips:** use the bundled parser for SCP-C ↔ JSON ↔ SCP-V conversions instead of doing them by hand — it validates syntax and is deterministic.

## Bundled script

`scripts/scp.py` — parser and renderer:

```bash
python scripts/scp.py render "G1>T:outline>A:editor=FAIL>RTY"   # → 🎯₁ ↓ 📋(outline) ↓ 🤖(editor) → ✗ → 🔄
python scripts/scp.py json   "G>T:script>A:writer=OK"           # → JSON AST
python scripts/scp.py decode "G>T:script>A:writer=OK"           # → natural language
python scripts/scp.py stats  "G>T:script>A:writer=OK"           # → bytes/element counts vs prose estimate
```

The script accepts multiple lines via stdin too: `cat state.scp | python scripts/scp.py render -`.

## Example

Input prose (28 words):

> The goal number 1 generated the task of outline, which was assigned to the editor agent. The agent executed the task and it failed and must be retried.

SCP-C (~12 tokens): `G1>T:outline>A:editor=FAIL>RTY`

SCP-V (for the dashboard): `🎯₁ ↓ 📋(outline) ↓ 🤖(editor) → ✗ → 🔄`

## Output format

When compressing for the user, always show: (1) the legend if extended codes were added, (2) the SCP-C block in a code fence, (3) a one-line savings estimate (entries × ~tokens saved − legend cost). Offer the SCP-V rendering but do not include it in anything destined for an LLM context.
