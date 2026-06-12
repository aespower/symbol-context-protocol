#!/usr/bin/env python3
"""SCP v0.3 benchmark — token counts for agent workflow state in 4 formats.

Usage:
  python run.py --vocab path/to/cl100k_base.tiktoken --name cl100k_base
If --vocab is omitted, tiktoken downloads o200k_base from the network.
"""
import argparse, base64, csv, json, random, sys

import tiktoken

PATS = {
    "cl100k_base": r"""'(?i:[sdmt]|ll|ve|re)|[^\r\n\p{L}\p{N}]?+\p{L}+|\p{N}{1,3}| ?[^\s\p{L}\p{N}]++[\r\n]*|\s*[\r\n]|\s+(?!\S)|\s+""",
    "o200k_base": r"""[^\r\n\p{L}\p{N}]?[\p{Lu}\p{Lt}\p{Lm}\p{Lo}\p{M}]*[\p{Ll}\p{Lm}\p{Lo}\p{M}]+(?i:'s|'t|'re|'ve|'m|'ll|'d)?|[^\r\n\p{L}\p{N}]?[\p{Lu}\p{Lt}\p{Lm}\p{Lo}\p{M}]+[\p{Ll}\p{Lm}\p{Lo}\p{M}]*(?i:'s|'t|'re|'ve|'m|'ll|'d)?|\p{N}{1,3}| ?[^\s\p{L}\p{N}]+[\r\n/]*|\s*[\r\n]+|\s+(?!\S)|\s+""",
}


def load_encoding(vocab_path, name):
    if not vocab_path:
        return tiktoken.get_encoding(name)
    ranks = {}
    with open(vocab_path, "rb") as f:
        for line in f:
            if line.strip():
                tok, rank = line.split()
                ranks[base64.b64decode(tok)] = int(rank)
    return tiktoken.Encoding(name=name, pat_str=PATS[name], mergeable_ranks=ranks,
                             special_tokens={"<|endoftext|>": len(ranks)})


TASKS = ["outline", "script", "thumbnail", "upload", "captions", "research",
         "edit", "schedule", "seo", "review", "publish", "analytics"]
AGENTS = ["writer", "editor", "uploader", "researcher", "designer", "analyst"]
PROSE_TPL = [
    "Goal {i} generated the task of {t}, which was assigned to the {a} agent. The agent executed it and the task {res_long}.",
    "For goal {i}, the system created a {t} task and handed it to the {a} agent, whose execution {res_long}.",
    "The {a} agent received the {t} task derived from goal {i} and after execution the task {res_long}.",
]
SCP_LEGEND = ("# SCP-C legend. Symbols: G=goal M=memory T=task A=agent X=execute "
              "OK=complete FAIL=failed RTY=retry GROW=growth REV=revenue VID=video. "
              "Grammar: > sequence (leads to / assigned to), = final result, + combination, "
              ":name parameter, [..] group, (..) metadata. One expression per line.")


def build_corpus(n=200, seed=42):
    rng = random.Random(seed)
    rows = []
    for i in range(1, n + 1):
        t, a = rng.choice(TASKS), rng.choice(AGENTS)
        ok = rng.random() < 0.75
        rows.append({
            "prose": rng.choice(PROSE_TPL).format(
                i=i, t=t, a=a,
                res_long="completed successfully" if ok else "failed and must be retried"),
            "json": json.dumps({"goal": i, "task": t, "agent": a,
                                "result": "ok" if ok else "fail",
                                "retry": not ok}, separators=(",", ":")),
            "toon_row": f"  {i},{t},{a},{'ok' if ok else 'fail'},{str(not ok).lower()}",
            "scp": f"G{i}>T:{t}>A:{a}=" + ("OK" if ok else "FAIL>RTY"),
        })
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vocab")
    ap.add_argument("--name", default="o200k_base", choices=list(PATS))
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--csv")
    args = ap.parse_args()
    enc = load_encoding(args.vocab, args.name)
    count = lambda s: len(enc.encode(s, disallowed_special=()))

    rows = build_corpus(args.n)
    docs = {
        "prose": "\n".join(r["prose"] for r in rows),
        "json_lines": "\n".join(r["json"] for r in rows),
        "toon": f"entries[{args.n}]{{goal,task,agent,result,retry}}:\n"
                + "\n".join(r["toon_row"] for r in rows),
        "scp_no_legend": "\n".join(r["scp"] for r in rows),
    }
    legend_tok = count(SCP_LEGEND)
    totals = {k: count(v) for k, v in docs.items()}
    totals["scp_with_legend"] = totals["scp_no_legend"] + legend_tok

    print(f"tokenizer={args.name} entries={args.n} scp_legend={legend_tok} tok")
    base = totals["prose"]
    for k in ["prose", "json_lines", "toon", "scp_no_legend", "scp_with_legend"]:
        print(f"{k:16} {totals[k]:6} tok  ({100 - round(totals[k]/base*100)}% vs prose)")

    # break-even curve vs prose and vs json
    if args.csv:
        with open(args.csv, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["entries", "prose", "json", "toon", "scp_incl_legend"])
            for n in [1, 2, 3, 5, 8, 10, 15, 20, 30, 50, 75, 100, 150, 200]:
                sub = rows[:n]
                w.writerow([n,
                    count("\n".join(r["prose"] for r in sub)),
                    count("\n".join(r["json"] for r in sub)),
                    count(f"entries[{n}]{{goal,task,agent,result,retry}}:\n" + "\n".join(r["toon_row"] for r in sub)),
                    count("\n".join(r["scp"] for r in sub)) + legend_tok])
        print(f"curve → {args.csv}")


if __name__ == "__main__":
    main()
