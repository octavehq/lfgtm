# Style Selection Reference

The positioning system uses the same CSS variable / style preset system as `/octave:deck`. Full preset definitions are in the deck skill's [style-presets.md](../../deck/references/style-presets.md).

Positioning documents default to strategic, executive-friendly presets.

## Style Menu

Present this menu if `--style` was not provided:

```
Pick a style for your positioning system:

DARK (recommended for strategy documents)
  1. midnight-pro      — Dark navy + blue accents. Executive feel. [DEFAULT]
  2. executive-dark    — Charcoal + gold. Premium boardroom.
  3. octave-brand      — Purple on navy. Product-aligned.

LIGHT
  4. paper-minimal     — Off-white + black type. Editorial.
  5. swiss-modern      — White + red accent. Clean minimal.
  6. soft-light        — Warm white + sage green. Calm.

VIBRANT
  7. solar-flare       — Deep orange gradients. Bold.
  8. aurora-gradient   — Purple-to-teal. Visionary.

OTHER
  9. Use my brand      — Extract from website or provide colors
  10. Match an existing doc — Reuse style from a previous /octave: document

Your choice (number or name, or press Enter for midnight-pro):
```

## Brand Discovery

If the user selects "Use my brand," follow the brand discovery flow from the deck skill (website extraction via browser-use or WebFetch, manual fallback).

If they select "Match an existing doc," ask for the file path and extract its CSS variables.
