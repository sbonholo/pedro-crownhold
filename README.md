# Crownhold

King/queen kingdom defense game (3D). Assets in `assets/` — see `assets/LICENSES.txt` for credits.

Made by **Pedro** with Claude.

- Play (Claude Artifact): https://claude.ai/artifact/SugNJ2bgZm8gadWWjiAad1
- Source: `index.html` (the whole game in one page). Serve the folder over HTTP (for example `npx serve .` or `python3 -m http.server`) and open it; opened straight from disk, the browser blocks the 3D models and HDR skies, so the game uses its built-in fallbacks.

## Layout
- `index.html`: the game (HTML, CSS and JS).
- `vendor/three/`: Three.js **r128** (`three.min.js`, `GLTFLoader.js`, `RGBELoader.js`, `SkeletonUtils.js`) copied from the `three@0.128.0` npm package (MIT, see `vendor/three/LICENSE`). The game loads nothing from CDNs.
- `vendor/fonts/`: Pirata One and Alegreya Sans, latin subset woff2 from `@fontsource` (SIL Open Font License, texts alongside).
- `assets/models/*.glb`, `assets/hdri/*.hdr`: binary models and HDR skies. `assets/textures/<set>/`: 1024 px textures plus a `_512` copy.

## Publishing the Claude Artifact
The artifact host only serves standard web types (no `.glb`/`.hdr`). Run `python3 tools/build-artifact.py`: it writes `dist/artifact/` with `ASSET_WRAPPED = true` and the models/skies as base64 `*.glb.json`/`*.hdr.json` wrappers. Publish `dist/artifact/index.html` with those wrappers plus `assets/textures`, `assets/LICENSES.txt` and `vendor/`.

## Loading and devices
- Phones use the 512 px textures and smaller shadow maps. Desktops start on the 512 px textures, then swap in the 1024 px ones in the background.
- The loading bar counts downloaded bytes.
- The game pauses, and the render loop and audio stop, while the tab is hidden.
- If something breaks, a small "Something went wrong - tap to reload" toast appears.

## Why Three.js is still r128
Moving to three@0.170 (ES modules) changes colour management, light units, tone-mapping shader chunks, `sRGBEncoding`/`RGBEEncoding` and the HDR loader. The game patches the tone-mapping shader and uses custom shaders, so the upgrade cannot be done in one pass without visual changes. r128 is kept and vendored locally. Upgrade it in a separate pass with side-by-side screenshots.

## Rules for this repo
This repo is Pedro's only. Keep all work on this game here — never in Dad's work repos (beija, money, Arborium, Salsa, Gymgosh, etc.).
