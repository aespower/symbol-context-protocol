# Video System SCP Example

## Natural Language

The system has a video production goal. A video agent executes the task. The output should support growth and revenue. The workflow completes successfully.

## SCP-C

```txt
G > T:VID > A:video > X = [GROW+REV] > OK
```

## SCP-V

```txt
🎯 ↓ 📋(🎬) ↓ 🤖(video) ↓ ⚡ → [📈 + 💰] → ✓
```

## Agent Communication

```txt
SCP-C: T:video_script > A:writer > X = OK
SCP-V: 📋(video_script) ↓ 🤖(writer) ↓ ⚡ → ✓
```

The video script task was assigned to the writer agent and completed.
