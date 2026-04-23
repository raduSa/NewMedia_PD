# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A real-time spatial audio controller with three components:

1. **page.html** — Browser UI: HTML5 Canvas with 4 draggable audio objectives. Tracks mouse position, calculates Euclidean distances to each objective, and streams JSON over WebSocket at ~60fps.
2. **server.py** — Python WebSocket server: receives distance data from the browser and forwards it as OSC messages to Pure Data.
3. **init_setup.pd** — Pure Data patch: OSC listener that routes incoming distance values to audio synthesis parameters.

## Running the Project

Requires Pure Data to be running with `init_setup.pd` loaded before starting the server.

```bash
# Activate the virtual environment
source .venv/Scripts/activate   # Windows Git Bash / bash
# .venv\Scripts\activate        # Windows cmd

# Start the WebSocket server
python server.py
```

Then open `page.html` directly in a browser (no HTTP server needed).

## Hardcoded Addresses

| Connection | Value |
|---|---|
| WebSocket server | `ws://localhost:8765` |
| OSC target (Pure Data) | `127.0.0.1:8000` |

## Data Flow

```
Browser mouse movement
  → distances JSON: [{id: "Obj_A", dist: 245.3}, ...]
  → WebSocket (port 8765)
  → server.py
  → OSC messages: /obj/Obj_A 245.3
  → Pure Data (UDP port 8000)
  → audio parameter control
```

## Dependencies

Installed in `.venv` (no requirements.txt):
- `websockets==16.0`
- `python-osc==1.10.2`

## Spatial Objectives (page.html)

Four fixed-position objectives on the 800×600 canvas:

| ID | Position | Label | Color |
|---|---|---|---|
| Obj_A | (200, 150) | Melody | Blue |
| Obj_B | (600, 150) | Rhythm 1 | Red |
| Obj_C | (200, 450) | Rhythm 2 | Yellow |
| Obj_D | (600, 450) | Ambience | Green |
