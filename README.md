# Domus Materiae — identity system

Style guide for the Domus Materiae brand. Palette, typography, motion tokens and the
nautilus construction are inherited from `nautilus-hero.html`.

Live version: https://claude.ai/code/artifact/565c03b6-f887-4d92-b78b-bf47184878f3

## The files

| File | What it is |
|---|---|
| `domus-materiae-style-guide.html` | **Open this one.** A complete HTML document. Double-click it, or serve it. No dependencies beyond Google Fonts. |
| `domus-materiae-style-guide.artifact.html` | Source for publishing as a Claude Artifact. Page content only — no `<!DOCTYPE>`, `<html>`, `<head>` or `<body>`, because the Artifact runtime supplies those. |
| `build-standalone.py` | Regenerates the standalone document from the artifact source. |

Edit the **artifact** file, then run:

    python3 build-standalone.py

Both files stay in sync that way. Do not edit the standalone directly — it gets overwritten.

## Why there are two files

The artifact source is deliberately not a valid standalone document. Served or opened
directly it has no doctype, so the browser falls into **quirks mode** — `svh` units stop
working and compositing changes, which makes the hero animation flash. If the hero ever
misbehaves, check `document.compatMode` first: it must be `CSS1Compat`.

## The hero

Two options, swipeable (drag, arrow keys, or the dots beside Rivedi):

- **Nautilus** — the proportion. A WebGL fragment shader: a height field (chamber dome,
  septum ridge, outer wall) gives real surface normals, driving diffuse + specular +
  ambient occlusion + a thin-film term. Growth lines are striations across the whorl.
  An SVG overlay carries the white spiral and the sezione aurea in Larice.
- **Anelli** — the material. The same growth law read as end grain: annual rings with
  wide earlywood and thin latewood rims, spacing varying year to year, radial checks
  widening out from the pith. Compiles lazily, only once someone swipes to it.

If WebGL is unavailable, an SVG path renderer takes over automatically.

Timing tokens (`--t-lines-out` 5.6s, `--t-text-in` 6.8s) are in the Token appendix.

## Build rules — these are not preferences

The Movimento section was removed from the guide, so this is the only record. Every one
of these cost real debugging.

1. **Inside the SVG, animate `fill-opacity` and `stroke-opacity` only** — never `opacity`
   or `transform` on a group. Covering the frame forces the shell to span 3280 × 3828
   user units, because the spiral opens 3× per turn and has to reach ~3.3× beyond the
   visible area. Promoting a group that size allocates a compositing layer from its full
   bounding box — roughly 9700 px on a large HiDPI display, past Chrome's 8192 px texture
   limit. Chrome then tiles the layer and evicts tiles, which reads as flashing. Paint
   properties never create a layer, so the problem cannot occur.

2. **The swell belongs on the `<svg>` element (or `.stage`), not the inner group.** Same
   motion, but the element is hero-sized, so the layer is bounded whatever the geometry does.

3. **Never clamp the radius in `pt()`.** `septum()` samples a control point half a turn
   away, so clamping throws the Béziers and tears the chambers into self-intersecting
   shapes. Truncating by *parameter* is safe; truncating by *radius* is not. Cost is
   handled by the `clipPath` at the viewBox instead.

4. **No CSS filters in the hero.** A `blur()` over the shell forces the whole stack to be
   re-filtered every frame for as long as anything underneath it moves.

5. **Septa are not radial spokes.** They lean forward by the 0.60 rad lead and bow
   concavely between the walls — 1.15 chambers of skew plus a 0.55 bow. Drawn at constant
   θ the shell reads as a flat fan.

6. **Serve with `Cache-Control: no-store`** while iterating (`serve.py` does this).
   `python -m http.server` lets the browser reuse a stale copy, which repeatedly made
   edits look like they had not landed.

## Still open

- The blur on the ending (`hSoften` used to carry `filter: blur(28px)`) was removed on
  request. Restoring it is a one-line change — but see build rule 4 first.
- The guide no longer documents logo misuse, photography direction, or motion. Those
  sections were removed deliberately; the rules above are what survived from Movimento.
