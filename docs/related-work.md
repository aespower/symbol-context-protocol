# Related Work — How SCP Compares

An honest comparison of SCP against existing context-optimization strategies (researched June 2026). Short version: several techniques achieve higher raw compression, but none occupies SCP's exact niche — a zero-infrastructure, deterministic, human-readable notation for **agent workflow state**.

## Comparison Table

| Strategy | Savings | How it works | vs SCP |
|---|---|---|---|
| **LLMLingua / LLMLingua-2** (Microsoft) | 4–20x on prose | A small model prunes low-information tokens from prompts | More efficient for arbitrary text, but lossy, requires extra model infrastructure, output not human-readable |
| **Context editing + memory tools** (Anthropic) | up to 84% in long agent sessions | Provider-native pruning/summarization of agent history | Bigger practical impact for agents; complementary to SCP, not a competitor |
| **TOON** (Token-Oriented Object Notation) | 40–60% vs JSON | Tabular, quote-free, brace-free format for uniform structured data | **Closest direct competitor to SCP-C** — published spec, SDK, benchmarks, 99.4% accuracy |
| **MetaGlyph** (arXiv 2601.07354) | variable | Symbolic metalanguage using mathematical symbols for instructions | Same family as SCP; academically validates using symbols with pretrained semantics |
| **Latent communication (Interlat)** | extreme (no text) | Agents exchange hidden states directly | Theoretically more efficient, but research-stage and zero human readability |

## Positioning

1. **vs TOON:** TOON solved compact, readable notation for *tabular data*. SCP targets *workflow and agent state* — sequences, assignments, results, retries — which TOON does not model. The formats are complementary: TOON for data payloads, SCP for execution state.
2. **vs MetaGlyph:** MetaGlyph argues that compact symbols with semantics the model already knows (math notation) compress instructions effectively. SCP's design rule — every dictionary code must be a single token with pretrained meaning (`FAIL`, `GROW`, not rare strings or digits) — follows the same principle, applied to operational state.
3. **vs statistical compression (LLMLingua):** different problem. LLMLingua compresses arbitrary prose with an auxiliary model and lossy output. SCP is deterministic, reversible, infrastructure-free, and human-auditable — at the cost of only applying to structured operational state.
4. **vs context engineering (compaction, memory tools):** these manage *what* stays in context; SCP optimizes *how* what stays is encoded. They stack: a compacted memory written in SCP-C is smaller than the same memory in prose.

## Sources

- [LLMLingua — Microsoft Research](https://www.microsoft.com/en-us/research/blog/llmlingua-innovating-llm-efficiency-with-prompt-compression/)
- [LLMLingua in production, 2026](https://tokenmix.ai/blog/llmlingua-prompt-compression-2026)
- [Prompt Compression: 8 Techniques (Morph)](https://www.morphllm.com/prompt-compression)
- [TOON specification](https://github.com/toon-format/toon)
- [TOON — InfoQ coverage](https://www.infoq.com/news/2025/11/toon-reduce-llm-cost-tokens/)
- [TOON vs JSON benchmark (arXiv 2603.03306)](https://arxiv.org/abs/2603.03306)
- [MetaGlyph — Semantic Compression via Symbolic Metalanguages (arXiv 2601.07354)](https://arxiv.org/html/2601.07354)
- [Interlat — latent-space agent communication (arXiv 2511.09149)](https://arxiv.org/pdf/2511.09149)
- [Agent context compression strategies (Zylos)](https://zylos.ai/research/2026-02-28-ai-agent-context-compression-strategies/)
- [State of AI Agent Memory 2026 (Mem0)](https://mem0.ai/blog/state-of-ai-agent-memory-2026)
