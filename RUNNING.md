# Running the project

## Order of operations

**1. Pure Data**
Open `init_setup.pd` in Pure Data and turn on audio (Ctrl+/ or Media → Audio On).
All subpatches (`pd_weights`, `pd_params`, `pd_atmosphere`, `pd_rhythm`, `pd_melody`, `pd_reverb`) load automatically. Parameters broadcast on patch load via `loadbang` inside `pd_params`.

**2. Python server**
```bash
source .venv/Scripts/activate   # Windows Git Bash
python server.py
```
The server listens for WebSocket connections on port 8765 and forwards distance data as OSC to Pure Data on UDP port 8000.

**3. Browser**
Open `page.html` directly in a browser (no HTTP server needed). Move the mouse over the canvas to start sending data.

## What you should hear
Audio starts as soon as Pure Data's audio is on. Sound changes as you move the mouse — closer to an objective raises its weight, which affects all three generators (atmosphere, rhythm, melody) simultaneously.

## Stopping
Close the browser tab, then Ctrl+C the Python server, then close Pure Data.
