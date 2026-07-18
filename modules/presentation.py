"""How a module looks — the mission-card gradient and glyph.

These are presentation, not content, so they live in code keyed by the module's
order_index rather than as columns on the Module table. Deriving them here means
no schema change and one place to restyle all six cards.
"""

# (violet, cyan) gradient endpoints, one per module position.
TILES = [
    ("#9b7bf8", "#22d3ee"),
    ("#7c5cf0", "#4fb8f5"),
    ("#a86af0", "#22d3ee"),
    ("#6d7bf5", "#35d6f0"),
    ("#b45cf0", "#5b8df5"),
    ("#8b5cf6", "#67e8f9"),
]

# Icon id (see templates/_icons.html) per module position.
ICONS = ["i-layers", "i-shield", "i-mail", "i-lock", "i-bolt", "i-clock"]


def decorate(module):
    """Attach presentation attributes to a Module for the templates.

    Also aliases `.index`/`.subtitle` onto the real model so it drops into the
    same `_module_tile.html` partial the marketing pages use (which was written
    against the placeholder dicts' key names).
    """
    i = (module.order_index - 1) % len(TILES)
    module.tile_a, module.tile_b = TILES[i]
    module.icon = ICONS[(module.order_index - 1) % len(ICONS)]
    module.index = module.order_index
    module.subtitle = module.description
    return module
