# Symbol Context Protocol Roadmap

## v0.1 — Concept Draft (done)

- Initial vision, first symbol dictionary, basic grammar, simple examples.

## v0.2 — Two-Layer Architecture (current)

- Canonical ASCII layer (SCP-C) for token efficiency.
- Visual emoji layer (SCP-V) as pure rendering for humans.
- Disambiguated grammar (`>` sequence vs `=` result).
- Honest token-cost documentation.

## v0.3 — Parser Prototype + Benchmark

- Python parser: SCP-C ↔ SCP-V ↔ JSON.
- Syntax validation.
- Token benchmark vs natural language and compact JSON (tiktoken), published in repo.

## v0.4 — Expanded Symbol Dictionary

- 100+ standardized codes organized by category.
- Naming conventions and per-symbol usage examples.

## v0.5 — Formal Grammar

- EBNF specification, nesting rules, reusable patterns.

## v0.6 — Knowledge Graph Mapping

- Symbols to nodes, operators to edges, metadata structure, graph database examples.

## v0.7 — SDKs

- Python package (parser, validation, graph export).
- JavaScript package (Node + browser, visual renderer).

## v0.8 — Integrations

- LangGraph, CrewAI, AutoGen, AIOS (memory, communication, workflow, tracking layers).

## v1.0 — SCP Standard

- Stable specification, frozen core grammar and dictionary, reference implementation.
