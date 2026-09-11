# Font cục bộ / Local font provenance

Downloaded 2026-09-11 from the official [Google Fonts repository](https://github.com/google/fonts).

- [Lora upstream files and SIL OFL 1.1](https://github.com/google/fonts/tree/main/ofl/lora): regular and italic variable TTF. Original copyright: The Lora Project Authors, 2011. **Lora is a Reserved Font Name.** The modified subset bundled here is renamed **Universe Serif**, including its internal family and PostScript names.
- [Noto Sans upstream files and SIL OFL 1.1](https://github.com/google/fonts/tree/main/ofl/notosans): normal variable TTF. Original copyright: The Noto Project Authors, 2022. No reserved font name in the bundled license.

Full licenses: `Lora-OFL.txt`, `NotoSans-OFL.txt`. Keep them with redistributed fonts. SHA-256 of the source and output files is recorded in `manifest.json`.

One-time preparation used fontTools to instantiate Lora at weight 400 (normal and real italic); Noto Sans keeps the 400–700 weight axis, with width fixed at 100. Files were subset to Latin, Latin Extended, combining diacritics, Latin Extended Additional (including all Vietnamese letters), punctuation and currency symbols, preserving shaping tables. Output is WOFF2. These fonts support both precomposed Vietnamese (NFC) and combining accents (NFD).

This preparation is already done: **no font build step, npm or Python is needed by the website**. Three local WOFF2 files cover all styles used. Decorative hearts/arrows may use a system symbol font; Vietnamese words use a single family per text style.

Change font declarations in `css/fonts.css`, and the `--font-body` / `--font-heading` stacks in `css/styles.css`. Both stacks end in system fallbacks verified for Vietnamese on the test machine. `font-display: swap` keeps text readable while loading or if requests fail. Preload only the body and upright heading fonts; the italic file loads when used.
