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
        "subtitle": "What a network actually is, and why yours is worth protecting.",
        "icon": "i-layers",
        "tile_a": "#9b7bf8",
        "tile_b": "#22d3ee",
    },
    {
        "index": 2,
        "title": "Recognising Cyber Threats",
        "subtitle": "The scams and attacks that really turn up in Australian workplaces.",
        "icon": "i-shield",
        "tile_a": "#7c5cf0",
        "tile_b": "#4fb8f5",
    },
    {
        "index": 3,
        "title": "Phishing & Social Engineering",
        "subtitle": "How to spot a fake email or phone call before you act on it.",
        "icon": "i-mail",
        "tile_a": "#a86af0",
        "tile_b": "#22d3ee",
    },
    {
        "index": 4,
        "title": "Secure Communication Practices",
        "subtitle": "Passwords, messages and files — handled safely, without the hassle.",
        "icon": "i-lock",
        "tile_a": "#6d7bf5",
        "tile_b": "#35d6f0",
    },
    {
        "index": 5,
        "title": "Firewall & Network Defence",
        "subtitle": "The tools quietly guarding your business, and how to keep them working.",
        "icon": "i-bolt",
        "tile_a": "#b45cf0",
        "tile_b": "#5b8df5",
    },
    {
        "index": 6,
        "title": "Incident Response",
        "subtitle": "If something goes wrong: who to call, and what to do first.",
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
    "items": [
        {
            "value": "84,700",
            "label": "cybercrime reports",
            "note": "made to the ASD in 2024–25",
        },
        {
            "value": "6 min",
            "label": "between reports",
            "note": "one lodged every six minutes, on average",
        },
        {
            "value": "$56,600",
            "label": "average cost",
            "note": "per report, for a small business",
        },
    ],
}
