# Session Memory Snapshot Example

The heterogeneous benchmark showed SCP's niche: ordered, mixed-type state. A session/project memory snapshot is exactly that. Instead of storing conversation history or prose summaries, store SCP-C state lines.

## Prose memory (~52 tokens)

> The user is building an open source project called Symbol Context Protocol to save tokens in AI systems. It currently has two layers (canonical and visual), version 0.2 is published, benchmarks were run, and the next step is the domain dictionary packs for v0.4.

## SCP-C memory (~25 tokens)

```txt
M:project=SCP
G=context_optimization
STATUS:v0.2>OK
T:benchmark=OK
T:dict_packs(target:v0.4)>RTY
```

Same operational content, ~50% fewer tokens, append-friendly (each new fact is one line), order-preserving (the history of the project reads top to bottom), and machine-parseable for graph export.

## Pattern

```txt
M:<key>=<value>          stable facts and preferences
STATUS:<version|phase>   where things stand
T:<name>=OK|FAIL>RTY     what was done / what's pending
?[..]>..                 standing decisions as rules
W:<name>=<v>             recorded signal strengths
```

Refresh the snapshot by rewriting lines, not appending duplicates — the snapshot is state, not a log.
