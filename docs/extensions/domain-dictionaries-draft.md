# SCP Extension Draft — Domain Dictionary Packs

**Status:** experimental draft, measured. Target: v0.4.

## Problem (measured)

The roadmap calls for 100+ standardized codes. A monolithic legend for ~100 codes costs **383 tokens per context** (o200k_base) — paid on every LLM call, eroding SCP's savings. Additionally, the heterogeneous benchmark showed verbose metadata (`(priority:high,deadline:d12)`) is SCP's biggest token leak (savings dropped from 49% to 26%).

## Design

The dictionary splits into a small always-on **core** plus opt-in **domain packs** declared per document:

```txt
# DICT video
# DICT business
```

- **Core (~11 codes + grammar):** 75 tokens. Always in the legend.
- **Each pack (~7-10 codes):** ~30 tokens. Loaded only if declared.
- Measured: core + 1 pack = **107 tokens vs 383 monolithic — 72% legend reduction** at 100-code scale.

### Example packs

```txt
# pack video:    HK=hook SCN=scene VO=voiceover SUB=subtitle RET=retention THB=thumbnail CTA=call-to-action
# pack business: INV=invoice LEAD=lead DEAL=deal TKT=ticket RFD=refund CHN=churn
# pack meta:     p=priority d=deadline(day) h=high l=low m=mid
```

### Short metadata keys (pack `meta`)

Packs may also standardize metadata keys/values:

```txt
v0.2: T:upload(priority:high,deadline:d12)
v0.4: T:upload(p:h,d:12)
```

Measured on the heterogeneous corpus: **10% fewer tokens on metadata-carrying entries** (804 → 724), 2% net overall including the +22-token pack legend; the gain grows with metadata density.

## Rules

1. Pack codes must follow the core single-token rule (verify with tiktoken).
2. A document's legend includes core + only the packs it declares.
3. Pack codes must not collide with core or with other declared packs.
4. Undeclared codes are a parser error (conformance: specification.md §5).

## Adoption criteria

Graduates to core spec with v0.4 when: (1) at least 3 packs defined and benchmarked, (2) parser support for `# DICT` declarations, (3) re-run of the heterogeneous benchmark confirms net savings ≥30% vs prose with packs enabled.
