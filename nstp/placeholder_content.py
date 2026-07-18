"""Placeholder content for the public pages.

TEMPORARY — Sprint 2 replaces this with real `modules.Module` rows and deletes
this file. It exists so the six module names live in ONE place rather than
being copy-pasted across the landing page, the modules page, the dashboard and
the styleguide, where they would immediately drift apart.

The titles are the six from the spec. The subtitles are ours: the spec's names
are accurate but they read like a syllabus, and our learners are non-technical
Australians who did not sign up for a syllabus. Title says what it is;
subtitle says why they should care, in words they'd use themselves.

The two hues per module feed --cy-tile-a / --cy-tile-b on the mission tiles, so
the six are distinguishable at a glance without a legend.
"""

MODULES = [
    {
        "index": 1,
        "title": "Network Security Fundamentals",
        "subtitle": "How networks work, and where yours is most exposed.",
        "icon": "i-layers",
        "tile_a": "#9b7bf8",
        "tile_b": "#22d3ee",
    },
    {
        "index": 2,
        "title": "Recognising Cyber Threats",
        "subtitle": "The tactics used against Australian organisations today.",
        "icon": "i-shield",
        "tile_a": "#7c5cf0",
        "tile_b": "#4fb8f5",
    },
    {
        "index": 3,
        "title": "Phishing & Social Engineering",
        "subtitle": "Identify fraudulent emails and calls before they succeed.",
        "icon": "i-mail",
        "tile_a": "#a86af0",
        "tile_b": "#22d3ee",
    },
    {
        "index": 4,
        "title": "Secure Communication Practices",
        "subtitle": "Handling passwords, messages and files securely, as routine.",
        "icon": "i-lock",
        "tile_a": "#6d7bf5",
        "tile_b": "#35d6f0",
    },
    {
        "index": 5,
        "title": "Firewall & Network Defence",
        "subtitle": "The defences protecting your business, and how to maintain them.",
        "icon": "i-bolt",
        "tile_a": "#b45cf0",
        "tile_b": "#5b8df5",
    },
    {
        "index": 6,
        "title": "Incident Response",
        "subtitle": "A clear plan for the first hour after something goes wrong.",
        "icon": "i-clock",
        "tile_a": "#8b5cf6",
        "tile_b": "#67e8f9",
    },
]

# Every figure below is from the ASD Annual Cyber Threat Report 2024-25
# (released October 2025), verified against asd.gov.au. Cited on the page with
# the reporting period, because a statistic without a date is just a vibe.
#
# NOTE FOR WHOEVER MAINTAINS THIS: ASD publishes annually, each October. When
# the 2025-26 report lands, update these three numbers AND the source label
# together. A stale figure presented as current is a false claim, not an
# out-of-date one.
THREAT_STATS = {
    "source": "ASD Annual Cyber Threat Report 2024–25",
    "source_url": "https://www.cyber.gov.au/about-us/view-all-content/reports-and-statistics/annual-cyber-threat-report-2024-2025",
    "period": "2024–25",
    # `value` is what renders — the real figure, always present in the HTML.
    # `count_to`/`prefix`/`suffix` let static/js/cybaroo.js animate up to it.
    # The split exists so the truthful number is the one in the markup and the
    # animation is the enhancement, rather than the page shipping a "0" that
    # only JavaScript can correct.
    "items": [
        {
            "value": "84,700",
            "count_to": 84700,
            "prefix": "",
            "suffix": "",
            "icon": "i-layers",
            "label": "cybercrime reports",
            # Just the fact and its period. An earlier draft of this line read
            # "most from ordinary organisations, not banks" — which sounds
            # right, reads well, and is not something ASD reports. If a claim
            # isn't in the source, it doesn't go on the page.
            "note": "made to the ASD in 2024–25",
        },
        {
            "value": "6 min",
            "count_to": 6,
            "prefix": "",
            "suffix": " min",
            "icon": "i-clock",
            "label": "between reports",
            "note": "one lodged every six minutes, around the clock, all year",
        },
        {
            "value": "$56,600",
            "count_to": 56600,
            "prefix": "$",
            "suffix": "",
            "icon": "i-bolt",
            "label": "the average bill",
            "note": "what one report costs a small business, on average",
        },
    ],
}
