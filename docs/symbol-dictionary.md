# SCP Symbol Dictionary — v0.2

SCP v0.2 defines two equivalent layers for every symbol:

- **SCP-C (canonical):** ASCII codes, token-efficient. Used between agents and in memory.
- **SCP-V (visual):** emoji rendering, human-friendly. Used in dashboards, logs, and docs. Never sent to the LLM.

| Code (SCP-C) | Render (SCP-V) | Name | Meaning | Category |
|---|---|---|---|---|
| `G` | 🎯 | Goal | Objective or desired outcome | Planning |
| `M` | 🧠 | Memory | Stored context or knowledge | Memory |
| `T` | 📋 | Task | Unit of work | Execution |
| `A` | 🤖 | Agent | AI agent or autonomous worker | Agents |
| `X` | ⚡ | Execute | Action or execution step | Execution |
| `OK` | ✓ | Complete | Successful result | State |
| `FAIL` | ✗ | Failed | Failed result | State |
| `RTY` | 🔄 | Retry | Repeat or retry action | State |
| `GROW` | 📈 | Growth | Growth objective | Business |
| `REV` | 💰 | Revenue | Monetization or income | Business |
| `VID` | 🎬 | Video | Video production or media output | Production |

## Examples

```txt
SCP-C: G > T            SCP-V: 🎯 ↓ 📋
A goal generates a task.

SCP-C: X = OK           SCP-V: ⚡ → ✓
Execution completed successfully.

SCP-C: X = FAIL > RTY   SCP-V: ⚡ → ✗ → 🔄
Execution failed and requires retry.

SCP-C: G = [GROW+REV]   SCP-V: 🎯 → [📈 + 💰]
The goal is growth and revenue.
```

## Why ASCII codes?

Emojis cost 2–4 tokens each in current tokenizers; ASCII codes cost 1. The canonical layer is what travels through model context, so it must be ASCII. Emojis remain as a pure rendering layer for humans.
