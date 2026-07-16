# Vendored fonts

Both families are vendored rather than loaded from Google Fonts: our CSP is
`default-src 'self'`, so any CDN request is blocked by the browser.

| Family | Weights | Used for | Licence |
|---|---|---|---|
| [Space Grotesk](https://github.com/floriankarsten/space-grotesk) | 400, 500, 700 | Headings, UI, body | SIL Open Font License 1.1 |
| [JetBrains Mono](https://github.com/JetBrains/JetBrainsMono) | 400, 700 | Numerals — XP, levels, streaks, timers | SIL Open Font License 1.1 |

Both licences permit redistribution, including bundled in a repository.
Files came from the `@fontsource` packages (latin subset only, ~96 KB total).

**Why these two.** Space Grotesk is geometric enough to read as technical
without tipping into novelty, and its lowercase stays legible at body sizes for
long study sessions. JetBrains Mono is reserved for *numbers that change* —
tabular figures mean a points counter ticking 990 → 1000 doesn't make the
layout jump.
