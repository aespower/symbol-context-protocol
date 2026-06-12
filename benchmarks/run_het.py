#!/usr/bin/env python3
"""SCP v0.3 heterogeneous benchmark — mixed agent state (workflows with optional
metadata, memory entries, conditional rules, group goals) in 4 formats.

TOON is given its best shot: entries are grouped by type into uniform tables;
variable-arity values are encoded as '|'-joined strings inside cells.

Usage: python run_het.py --vocab path/to/o200k_base.tiktoken --name o200k_base
"""
import argparse, json, random
from run import load_encoding, PATS, SCP_LEGEND

TASKS = ["outline","script","thumbnail","upload","captions","research","edit","schedule","seo","review"]
AGENTS = ["writer","editor","uploader","researcher","designer","analyst"]
SIGNALS = ["FAIL","HIGH","LOW","G","VID","REV","GROW","M:short_pref","OK"]
PREFS = [("user_pref","VID+retention"),("tone","casual+short"),("schedule","daily+morning"),
         ("audience","beginners+spanish"),("platform","tiktok+reels")]


def build(n_std=80, n_meta=40, n_mem=30, n_rule=30, n_group=20, seed=42):
    rng = random.Random(seed)
    E = []
    for i in range(1, n_std+1):
        t,a = rng.choice(TASKS), rng.choice(AGENTS); ok = rng.random()<.75
        E.append(("wf", dict(i=i,t=t,a=a,ok=ok)))
    for i in range(n_std+1, n_std+n_meta+1):
        t,a = rng.choice(TASKS), rng.choice(AGENTS); ok = rng.random()<.75
        pr = rng.choice(["high","low","mid"]); dl = f"d{rng.randint(1,28)}"
        E.append(("wfm", dict(i=i,t=t,a=a,ok=ok,pr=pr,dl=dl)))
    for i in range(n_mem):
        k,v = rng.choice(PREFS)
        E.append(("mem", dict(k=f"{k}_{i}", v=v)))
    for i in range(n_rule):
        cond = rng.sample(SIGNALS, rng.randint(2,3))
        cons = rng.choice(["RTY", "A:video", "T:short_video", "OK(skip)"])
        E.append(("rule", dict(c=cond, q=cons)))
    for i in range(n_group):
        g = rng.sample(["GROW","REV","VID","OK"], rng.randint(2,3))
        E.append(("grp", dict(i=i, g=g)))
    rng.shuffle(E)
    return E


def to_prose(k, d):
    if k=="wf":  return f"Goal {d['i']} generated the task of {d['t']}, assigned to the {d['a']} agent, and execution {'completed successfully' if d['ok'] else 'failed and must be retried'}."
    if k=="wfm": return f"Goal {d['i']} generated the {d['t']} task with {d['pr']} priority and deadline {d['dl']}, assigned to the {d['a']} agent; execution {'completed successfully' if d['ok'] else 'failed and must be retried'}."
    if k=="mem": return f"Remember that the {d['k'].replace('_',' ')} is {d['v'].replace('+',' with ')}."
    if k=="rule":return f"If {' and '.join(d['c'])} then {d['q']}."
    if k=="grp": return f"Goal {d['i']} aims at {' and '.join(d['g'])} combined."


def to_json(k, d):
    m = {"wf":  lambda: {"type":"wf","goal":d['i'],"task":d['t'],"agent":d['a'],"result":"ok" if d['ok'] else "fail","retry":not d['ok']},
         "wfm": lambda: {"type":"wf","goal":d['i'],"task":d['t'],"agent":d['a'],"meta":{"priority":d['pr'],"deadline":d['dl']},"result":"ok" if d['ok'] else "fail","retry":not d['ok']},
         "mem": lambda: {"type":"memory","key":d['k'],"value":d['v'].split("+")},
         "rule":lambda: {"type":"rule","if":d['c'],"then":d['q']},
         "grp": lambda: {"type":"goal","goal":d['i'],"targets":d['g']}}
    return json.dumps(m[k](), separators=(",",":"))


def to_scp(k, d):
    if k=="wf":  return f"G{d['i']}>T:{d['t']}>A:{d['a']}=" + ("OK" if d['ok'] else "FAIL>RTY")
    if k=="wfm": return f"G{d['i']}>T:{d['t']}(priority:{d['pr']},deadline:{d['dl']})>A:{d['a']}=" + ("OK" if d['ok'] else "FAIL>RTY")
    if k=="mem": return f"M:{d['k']}={d['v']}"
    if k=="rule":return f"?[{'+'.join(d['c'])}]>{d['q']}"
    if k=="grp": return f"G{d['i']}=[{'+'.join(d['g'])}]"


def to_toon(entries):
    """Best-effort TOON: one uniform table per entry type."""
    by = {}
    for k,d in entries: by.setdefault(k,[]).append(d)
    out=[]
    if "wf" in by:
        out.append(f"workflows[{len(by['wf'])}]{{goal,task,agent,result,retry}}:")
        out += [f"  {d['i']},{d['t']},{d['a']},{'ok' if d['ok'] else 'fail'},{str(not d['ok']).lower()}" for d in by['wf']]
    if "wfm" in by:
        out.append(f"workflowsMeta[{len(by['wfm'])}]{{goal,task,agent,priority,deadline,result,retry}}:")
        out += [f"  {d['i']},{d['t']},{d['a']},{d['pr']},{d['dl']},{'ok' if d['ok'] else 'fail'},{str(not d['ok']).lower()}" for d in by['wfm']]
    if "mem" in by:
        out.append(f"memory[{len(by['mem'])}]{{key,value}}:")
        out += [f"  {d['k']},{d['v'].replace('+','|')}" for d in by['mem']]
    if "rule" in by:
        out.append(f"rules[{len(by['rule'])}]{{if,then}}:")
        out += [f"  {'|'.join(d['c'])},{d['q']}" for d in by['rule']]
    if "grp" in by:
        out.append(f"goals[{len(by['grp'])}]{{goal,targets}}:")
        out += [f"  {d['i']},{'|'.join(d['g'])}" for d in by['grp']]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vocab"); ap.add_argument("--name", default="o200k_base", choices=list(PATS))
    args = ap.parse_args()
    enc = load_encoding(args.vocab, args.name)
    count = lambda s: len(enc.encode(s, disallowed_special=()))

    E = build()
    legend_ext = SCP_LEGEND + " Extensions: ?[..]>X conditional rule, W:name=v weight."
    docs = {
        "prose": "\n".join(to_prose(k,d) for k,d in E),
        "json_lines": "\n".join(to_json(k,d) for k,d in E),
        "toon_grouped": to_toon(E),
        "scp": "\n".join(to_scp(k,d) for k,d in E),
    }
    legend = count(legend_ext)
    print(f"tokenizer={args.name} entries={len(E)} scp_legend={legend}")
    base = count(docs["prose"])
    for k,v in docs.items():
        t = count(v) + (legend if k=="scp" else 0)
        label = k + ("+legend" if k=="scp" else "")
        print(f"{label:14} {t:6} tok ({100-round(t/base*100):3}% vs prose)")
    # nota: TOON agrupado pierde el orden global de las entradas; SCP/JSON/prosa lo conservan
    print("\nNote: grouping destroys global entry order in TOON; SCP/JSON/prose preserve it.")


if __name__ == "__main__":
    main()
