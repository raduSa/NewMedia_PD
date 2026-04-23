# Audio Generators Overview

All three generators receive the same four normalized weights (w_A, w_B, w_C, w_D) from `pd_weights`. These weights always sum to 1 and are derived from the player's Euclidean distance to each objective using a softmax-style formula: `w_i = exp(-0.008 * d_i) / sum(exp(-0.008 * d_j))`. Closer objectives get higher weights.

---

## Atmosphere (`pd_atmosphere`)

A continuous ambient texture running at all times under the other layers.

Each of the four objectives produces a band of filtered noise. The noise is passed through a `vcf~` (voltage-controlled filter) tuned to that objective's atmospheric root note — four MIDI values spread across four octaves (36, 55, 72, 84 — roughly 65 Hz, 196 Hz, 523 Hz, 1047 Hz). The Q (resonance) of each filter is fixed at patch load: voice A is broad (Q=15), B and C are moderate (Q=20, Q=30), D is narrow (Q=10). This gives each band a distinct timbral character: A is a low rumble, B a mid hum, C a bright shimmer, D a tight sub tone.

The weight controls amplitude only — a voice with w=0 fades to silence, w=1 plays at full level. The weight is scaled by 0.5 before smoothing (so max amplitude is half), then ramped over 100ms via `line~` to avoid clicks. All four bands are summed and attenuated by a master gain of 0.2.

Because the atmosphere is always on, it establishes the sonic environment continuously. The spatial blend — which timbral bands dominate — shifts in real time as the player moves.

---

## Rhythm (`pd_rhythm`)

A gated percussion layer that activates only when an objective's weight crosses a threshold.

Each voice uses a different noise character and envelope to represent a distinct percussive sound:
- **A** — low bass thud: low-pass filtered noise at 200 Hz, 200ms decay
- **B** — mid snap: band-pass filtered noise centered at 800 Hz, 80ms decay
- **C** — high crisp tick: high-pass filtered noise above 2000 Hz, 40ms decay
- **D** — sub thud: very low-pass filtered noise at 80 Hz, 300ms decay

A voice only runs when its weight exceeds **0.25**. Since equal weights are 0.25 each, this means a voice activates when its objective is at least as prominent as the equal-weight baseline. The gate uses `change` to detect flips, so the metronome starts/stops cleanly rather than toggling every frame. Beat intervals come from `r tempo_X` (set by pd_params: A=600ms, B=450ms, C=300ms, D=800ms).

On each beat, a random number gates a `sel 0` — only index 0 fires the hit, giving a probability of 1-in-N per beat (N is 4, 3, 2, or 6 depending on voice). This means voices don't hit every beat; they have a built-in sparse, stochastic rhythm. The hit envelope is applied via `line~`, then multiplied by the raw weight for amplitude scaling. This means two active voices can play simultaneously at different volumes.

---

## Melody (`pd_melody`)

A pitched melodic layer where amplitude sharpening causes the dominant objective's voice to stand out.

Before doing anything else, each incoming weight is **squared** (`w^2`). This compresses quiet voices dramatically — at equal weights of 0.25, each squares to 0.0625; if one voice reaches 0.7, it squares to 0.49 while others stay near zero. The effect is a soft winner-takes-most behavior without any explicit argmax logic.

Each voice plays notes from a **pentatonic scale** built on that objective's root note (set by pd_params: A=60, B=62, C=64, D=67 — MIDI C4, D4, E4, G4). On each beat, a random scale degree 0–4 is chosen and mapped to semitone intervals [0, 2, 4, 7, 9]. This is added to the root note and converted to a frequency for an oscillator. Because all four voices use the same interval structure, any combination of simultaneously playing voices will always be harmonically consonant.

The gate threshold is lower than rhythm (**0.1**), so melody voices blend more readily — multiple voices can play at once, creating harmonized lines when the player is equidistant from several objectives. Beat timing comes from the same tempo bus as rhythm. The note envelope is a sharp attack with a decay matching the tempo (A=600ms, B=400ms, C=300ms, D=800ms), giving a plucked character. Each voice's audio is then multiplied by its smoothed w^2 amplitude. Master output gain is 0.3.

---

## Mixing

The three generators feed into `init_setup.pd` where atmosphere and rhythm are summed first, then melody is added to that mix, and the result goes to the DAC. There is no further EQ or compression — the amplitude controls within each generator handle the blend.
