"""How a module looks — the mission-card gradient and glyph.

These are presentation, not content, so they live in code keyed by the module's
order_index rather than as columns on the Module table. Deriving them here means
no schema change and one place to restyle all six cards.
"""

# Matte (hi, deep) gradient endpoints, one per module position. Cyan / teal /
# steel-cyan family, so the six cards read as a cohesive set with variety in the
# Cyan & Teal command-console palette.
TILES = [
    ("#00d9ff", "#0899b8"),  # cyan
    ("#00e5cc", "#0a9e8c"),  # teal
    ("#33c1ff", "#0e6f9e"),  # sky-cyan
    ("#2fe0d0", "#0f8f88"),  # aqua
    ("#5ab5d6", "#245e78"),  # steel-cyan
    ("#3aa0ff", "#1a5fb0"),  # azure
]

# Icon id (see templates/_icons.html) per module position.
ICONS = ["i-layers", "i-shield", "i-mail", "i-lock", "i-bolt", "i-clock"]

# Bespoke per-module emblem (a mark drawn for each module's theme), used by the
# module-path roadmap. Falls back to ICONS by position for any 7th+ module.
EMBLEMS = ["i-mod-1", "i-mod-2", "i-mod-3", "i-mod-4", "i-mod-5", "i-mod-6"]


def decorate(module):
    """Attach presentation attributes to a Module for the templates.

    Also aliases `.index`/`.subtitle` onto the real model so it drops into the
    same `_module_tile.html` partial the marketing pages use (which was written
    against the placeholder dicts' key names).
    """
    i = (module.order_index - 1) % len(TILES)
    module.tile_a, module.tile_b = TILES[i]
    module.icon = ICONS[(module.order_index - 1) % len(ICONS)]
    module.emblem = EMBLEMS[(module.order_index - 1) % len(EMBLEMS)]
    module.index = module.order_index
    module.subtitle = module.description
    return module
