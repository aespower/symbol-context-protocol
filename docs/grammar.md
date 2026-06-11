# SCP Grammar — v0.2

This document defines the grammar for Symbol Context Protocol v0.2. Every operator has a canonical ASCII form (SCP-C) and a visual rendering (SCP-V).

## Core Operators

| SCP-C | SCP-V | Name | Meaning |
|---|---|---|---|
| `>` | ↓ | Sequence | One element leads to / is assigned to the next |
| `=` | → | Result | The expression produces this final result |
| `+` | + | Combination | Two or more elements combined |
| `:` | : | Parameter | Assigns a name or value to a symbol |
| `[ ]` | [ ] | Group | Groups symbols or expressions |
| `( )` | ( ) | Metadata | Adds contextual metadata |

**Change from v0.1:** the operators ↓ ("leads to") and → ("produces") overlapped. In v0.2, `>` chains workflow steps; `=` marks exclusively the final result of an execution.

## Sequence

```txt
SCP-C: G > T          SCP-V: 🎯 ↓ 📋
```

A goal leads to a task.

## Result

```txt
SCP-C: X = OK         SCP-V: ⚡ → ✓
```

Execution produces completion.

## Combination

```txt
SCP-C: GROW+REV       SCP-V: 📈 + 💰
```

## Parameter

```txt
SCP-C: T:script       SCP-V: 📋(script)
```

A task named "script".

## Metadata

```txt
SCP-C: T:script(priority:high)
```

A task with high priority.

## Patterns

```txt
Standard workflow:  G > T > A > X = OK
                    🎯 ↓ 📋 ↓ 🤖 ↓ ⚡ → ✓

Failure + retry:    G > T > A > X = FAIL > RTY
                    🎯 ↓ 📋 ↓ 🤖 ↓ ⚡ → ✗ → 🔄

Business goal:      G = [GROW+REV]
                    🎯 → [📈 + 💰]

Persistent memory:  M:user_pref = VID+retention
                    🧠(user_pref): 🎬 + retention
```
