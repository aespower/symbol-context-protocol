#!/usr/bin/env python3
"""SCP v0.2 parser — Symbol Context Protocol.

Converts between SCP-C (canonical ASCII), JSON, SCP-V (emoji render),
and natural language. Spec: https://github.com/aespower/symbol-context-protocol
"""
import json
import re
import sys

DICT = {
    "G": ("\U0001F3AF", "Goal"),      "M": ("\U0001F9E0", "Memory"),
    "T": ("\U0001F4CB", "Task"),      "A": ("\U0001F916", "Agent"),
    "X": ("⚡", "Execute"),       "OK": ("✓", "Complete"),
    "FAIL": ("✗", "Failed"),     "RTY": ("\U0001F504", "Retry"),
    "GROW": ("\U0001F4C8", "Growth"), "REV": ("\U0001F4B0", "Revenue"),
    "VID": ("\U0001F3AC", "Video"),
}
SUBSCRIPTS = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")

TOKEN_RE = re.compile(r"""
    (?P<code>[A-Z]+)(?P<index>\d+)?          # symbol code, optional index
    (?::(?P<param>[\w\-]+))?                 # :param
    (?:\((?P<meta>[^)]*)\))?                 # (metadata)
""", re.VERBOSE)


def parse_element(text):
    text = text.strip()
    if text.startswith("[") and text.endswith("]"):
        return {"group": [parse_element(p) for p in text[1:-1].split("+")]}
    m = TOKEN_RE.fullmatch(text)
    if not m or m.group("code") not in DICT:
        raise ValueError(f"Unknown SCP element: {text!r}")
    el = {"symbol": m.group("code"), "name": DICT[m.group("code")][1]}
    if m.group("index"):
        el["index"] = int(m.group("index"))
    if m.group("param"):
        el["param"] = m.group("param")
    if m.group("meta"):
        el["meta"] = m.group("meta")
    return el


def parse_line(line):
    """G1>T:x>A:y=FAIL>RTY  ->  {'sequence': [...], 'result': [...]}"""
    line = line.strip()
    if not line:
        return None
    # split top-level on '=' (result), respecting brackets
    depth, eq = 0, -1
    for i, ch in enumerate(line):
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
        elif ch == "=" and depth == 0:
            eq = i
            break
    seq_part = line if eq < 0 else line[:eq]
    res_part = None if eq < 0 else line[eq + 1:]

    def split_chain(part):
        out, depth, cur = [], 0, ""
        for ch in part:
            if ch in "([":
                depth += 1
            elif ch in ")]":
                depth -= 1
            if ch == ">" and depth == 0:
                out.append(cur)
                cur = ""
            else:
                cur += ch
        out.append(cur)
        return [parse_element(p) for p in out if p.strip()]

    node = {"sequence": split_chain(seq_part)}
    if res_part is not None:
        node["result"] = split_chain(res_part)
    return node


def el_to_v(el):
    if "group" in el:
        return "[" + " + ".join(el_to_v(e) for e in el["group"]) + "]"
    s = DICT[el["symbol"]][0]
    if "index" in el:
        s += str(el["index"]).translate(SUBSCRIPTS)
    if "param" in el:
        s += f"({el['param']})"
    if "meta" in el:
        s += f"({el['meta']})"
    return s


def el_to_text(el):
    if "group" in el:
        return " and ".join(el_to_text(e) for e in el["group"])
    s = DICT[el["symbol"]][1].lower()
    if "index" in el:
        s += f" #{el['index']}"
    if "param" in el:
        s += f" '{el['param']}'"
    if "meta" in el:
        s += f" ({el['meta']})"
    return s


def render(node):
    out = " ↓ ".join(el_to_v(e) for e in node["sequence"])
    if "result" in node:
        out += " → " + " → ".join(el_to_v(e) for e in node["result"])
    return out


def decode(node):
    parts = [el_to_text(e) for e in node["sequence"]]
    s = " leads to ".join(parts)
    if "result" in node:
        s += ", producing " + ", then ".join(el_to_text(e) for e in node["result"])
    return s.capitalize() + "."


def stats(lines):
    nodes = [parse_line(l) for l in lines if l.strip()]
    n_el = sum(len(n["sequence"]) + len(n.get("result", [])) for n in nodes if n)
    scp_bytes = sum(len(l.encode()) for l in lines)
    prose_est = n_el * 5 * 1.3  # ~5 words/element, 1.3 tok/word
    scp_est = n_el * 2          # element + operator
    return {
        "entries": len(nodes), "elements": n_el, "scp_bytes": scp_bytes,
        "est_tokens_scp": round(scp_est),
        "est_tokens_prose_equiv": round(prose_est),
        "est_savings_pct": round(100 - scp_est / prose_est * 100) if prose_est else 0,
    }


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        print("Usage: scp.py {render|json|decode|stats} 'EXPR' | -")
        sys.exit(1)
    cmd, arg = sys.argv[1], sys.argv[2]
    lines = sys.stdin.read().splitlines() if arg == "-" else [arg]
    if cmd == "stats":
        print(json.dumps(stats(lines), indent=2))
        return
    for line in lines:
        node = parse_line(line)
        if node is None:
            continue
        if cmd == "render":
            print(render(node))
        elif cmd == "json":
            print(json.dumps(node, ensure_ascii=False))
        elif cmd == "decode":
            print(decode(node))
        else:
            sys.exit(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
