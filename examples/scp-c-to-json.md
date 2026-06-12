# SCP-C ↔ JSON Conversion Example

Using the reference parser: `python skills/scp-context-optimizer/scripts/scp.py json "EXPR"`.

## Simple workflow

SCP-C:

```txt
G>T:script>A:writer=OK
```

JSON:

```json
{"sequence": [
   {"symbol": "G", "name": "Goal"},
   {"symbol": "T", "name": "Task", "param": "script"},
   {"symbol": "A", "name": "Agent", "param": "writer"}],
 "result": [{"symbol": "OK", "name": "Complete"}]}
```

## Failure with retry and metadata

SCP-C:

```txt
G2>T:upload(priority:high)>A:uploader=FAIL>RTY
```

JSON:

```json
{"sequence": [
   {"symbol": "G", "name": "Goal", "index": 2},
   {"symbol": "T", "name": "Task", "param": "upload", "meta": "priority:high"},
   {"symbol": "A", "name": "Agent", "param": "uploader"}],
 "result": [
   {"symbol": "FAIL", "name": "Failed"},
   {"symbol": "RTY", "name": "Retry"}]}
```

## Group as result

SCP-C:

```txt
G=[GROW+REV]
```

JSON:

```json
{"sequence": [{"symbol": "G", "name": "Goal"}],
 "result": [{"group": [
   {"symbol": "GROW", "name": "Growth"},
   {"symbol": "REV", "name": "Revenue"}]}]}
```

## Other directions

```bash
scp.py render "G>T:script>A:writer=OK"   # → 🎯 ↓ 📋(script) ↓ 🤖(writer) → ✓
scp.py decode "G>T:script>A:writer=OK"   # → Goal leads to task 'script' leads to agent 'writer', producing complete.
scp.py stats  -                          # ← multiple lines via stdin; token/byte savings estimate
```
