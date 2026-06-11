# Symbol Context Protocol Concept

> **v0.2 note:** SCP now uses a two-layer architecture. The canonical layer (SCP-C) is dense ASCII for token efficiency; emojis (SCP-V) are a pure rendering layer for humans and never travel through model context. Emoji examples below are the visual layer. See the README and docs/grammar.md.

## Overview

Symbol Context Protocol, or SCP, is an open source proposal for representing AI context using symbols, compact structures, and graph-friendly syntax.

The central idea is simple: large language models often consume too much context because goals, tasks, memory, agents, and execution states are repeatedly described using long natural language.

SCP introduces a symbolic layer that compresses meaning while preserving readability.

## What SCP Is

SCP is:

- A symbolic context representation system.
- A compact communication layer for AI agents.
- A memory-friendly format for AI Operating Systems.
- A graph-compatible structure for knowledge representation.
- A human-readable protocol for goals, tasks, agents, execution, and results.

## What SCP Is Not

SCP is not:

- A replacement for human language.
- A programming language.
- A prompt template.
- A closed standard.
- A model-specific format.

## Core Idea

Natural language:

```txt
The video agent should execute the task of creating content focused on growth and monetization.
```

SCP:

```txt
🤖🎬 ⚡ 📋 → 📈 + 💰
```

Both can express a similar intention.

The SCP version is shorter, visual, and easier to map into a knowledge graph.

## Design Philosophy

1. Compress meaning.
2. Preserve human readability.
3. Remain compatible with current LLMs.
4. Support graph-based reasoning.
5. Improve agent coordination.

## Basic Architecture

```txt
Goal Engine
↓
Knowledge Graph
↓
SCP
↓
Agents
↓
Execution
```

## Mission

The mission of SCP is to create an open protocol for representing knowledge, goals, memory, execution, and agent coordination in a compact, visual, and efficient way.
