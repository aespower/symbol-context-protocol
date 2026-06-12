# SCP Specification — v0.2 (Draft)

Formal definition of the Symbol Context Protocol canonical layer (SCP-C). The visual layer (SCP-V) is a deterministic rendering of SCP-C and adds no semantics.

## 1. Document structure

An SCP document is a sequence of UTF-8 lines. Each non-empty line is one **expression**. Lines starting with `#` are comments and must be ignored by parsers.

## 2. Grammar (EBNF)

```ebnf
document    = { line } ;
line        = comment | expression | empty ;
comment     = "#" , { any-char } ;
expression  = chain , [ "=" , chain ] ;
chain       = element , { ">" , element } ;
element     = symbol | group ;
group       = "[" , element , { "+" , element } , "]" ;
symbol      = code , [ index ] , [ ":" , param ] , [ "(" , meta , ")" ] ;
code        = upper-letter , { upper-letter } ;        (* must exist in dictionary *)
index       = digit , { digit } ;
param       = identifier ;                              (* [A-Za-z0-9_-]+ *)
meta        = key , ":" , value , { "," , key , ":" , value } ;
```

## 3. Semantics

- `>` (sequence): the left element leads to / is assigned to the right element. Left-associative.
- `=` (result): everything left of `=` is the workflow; everything right is its outcome. At most one top-level `=` per expression.
- `+` (combination): elements that occur together. Only valid inside groups or as a result.
- `:param` names a specific instance (`T:script` = the task called "script").
- `(meta)` attaches key:value pairs that parsers must preserve but may ignore.
- An `index` distinguishes instances of the same symbol (`G1`, `G2`).

## 4. Dictionary requirements

Every code must satisfy:

1. **Single-token rule:** the code must encode to exactly 1 token in mainstream tokenizers (verify with tiktoken). Prefer short common English words/abbreviations. Rare strings split into multiple tokens; digits collide with `index`.
2. **Pretrained semantics:** prefer codes whose plain-English meaning matches the SCP meaning (`FAIL`, `GROW`), so the model interprets them correctly even with a minimal legend.
3. **Uniqueness:** no code may be a prefix of another code in the same document.

Extensions are declared in a legend block at the top of a document:

```txt
# DICT IMG=image SEO=seo-optimization
```

## 5. Conformance

A conforming parser must: (a) parse the grammar above, (b) reject unknown codes with an error naming the offending element, (c) round-trip SCP-C → JSON → SCP-C without loss. Reference implementation: [`skills/scp-context-optimizer/scripts/scp.py`](../skills/scp-context-optimizer/scripts/scp.py).

## 6. JSON mapping

Each expression maps to an object with `sequence` (array of elements) and optional `result` (array). Elements carry `symbol`, `name`, and optionally `index`, `param`, `meta`. Groups map to `{"group": [elements]}`. See [examples/scp-c-to-json.md](../examples/scp-c-to-json.md).
