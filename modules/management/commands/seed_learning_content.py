"""Seed the six modules, their lessons and their simulations.

Idempotent: run it as often as you like. Everything keys on a natural unique
field (module order_index, lesson number, one simulation per module) via
get_or_create / update_or_create, so re-running updates in place rather than
duplicating.

The lesson bodies are CLEARLY-MARKED PLACEHOLDERS — the real ≥800-word lessons
come after the system is signed off. They are deliberately rich (headings,
lists, a callout, a table) so the reading experience and the sanitiser are
exercised against real structure, not a single paragraph.

Content is data, not schema: this is a management command, not a data migration,
so it stays re-runnable and out of the migration history.
"""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from authentication.models import User
from modules.content import (
    module_five,
    module_four,
    module_one,
    module_six,
    module_three,
    module_two,
)
from modules.gamification import POINTS_PER_LESSON
from modules.models import Lesson, LessonTask, Module, Simulation
from quizzes.models import Answer, Question, Quiz

# Task points are authored against a 10-XP-per-lesson base (each lesson's tasks
# sum to 10 in the content files). The live economy scales that up, so multiply
# every task's points by the same factor here — the tasks then sum to
# POINTS_PER_LESSON exactly, and the in-lesson XP bar matches what the lesson banks.
_POINTS_SCALE = POINTS_PER_LESSON // 10

# Modules with finished, interactive content (LESSONS + QUIZ), keyed by
# order_index. Adding a module is data-only: write modules/content/module_N.py in
# the Module 1 shape and register it here. Anything not listed falls back to the
# rich placeholder until its turn.
CONTENT = {
    1: module_one,
    2: module_two,
    3: module_three,
    4: module_four,
    5: module_five,
    6: module_six,
}

# (title, description, difficulty, four lesson titles)
MODULES = [
    (
        "Network Security Fundamentals",
        "How networks work, and where yours is most exposed.",
        Module.Difficulty.BEGINNER,
        [
            "What a network is, and what you protect",
            "How attacks actually happen",
        ],
    ),
    (
        "Recognising Cyber Threats",
        "Malware and how it gets in, the real Australian breaches, and how to react.",
        Module.Difficulty.BEGINNER,
        [
            "Know the threats: malware, and how it gets in",
            "When it goes wrong: ransomware, breaches, and reacting",
        ],
    ),
    (
        "Phishing & Social Engineering",
        "The con behind the click, across every channel, and how to spot it.",
        Module.Difficulty.INTERMEDIATE,
        [
            "The con, and the channels it comes through",
            "Read it like an analyst: spot, verify, report",
        ],
    ),
    (
        "Secure Communication Practices",
        "What secure really means, and how to communicate that way as routine.",
        Module.Difficulty.INTERMEDIATE,
        [
            "Before you hit send: what 'secure' really means",
            "Sharing safely: files, links, and Wi-Fi",
        ],
    ),
    (
        "Firewall & Network Defence",
        "The defences around your whole business, and how to spot where they are missing.",
        Module.Difficulty.ADVANCED,
        [
            "The firewall: reading the rules that guard your network",
            "Defence in depth: segment, connect safely, and watch for trouble",
        ],
    ),
    (
        "Incident Response",
        "A calm, six-phase plan for what to do when something goes wrong.",
        Module.Difficulty.ADVANCED,
        [
            "When the alert fires: detect and contain",
            "Clean up, come back, and the law: eradicate, recover, review",
        ],
    ),
]

# A short motto/framing line per module (by order_index), shown as an accent
# eyebrow on the module overview.
TAGLINES = {
    1: "Know your network. Guard every door.",
    2: "Name the threat. Stop the spread.",
    3: "They hack the human. Verify anyway.",
    4: "Before you hit send, think.",
    5: "Set the rules. Watch them hold.",
    6: "Panic is optional. A plan is not.",
}


def _placeholder_body(module_title, lesson_title):
    return f"""
<p><strong>Placeholder lesson.</strong> This stands in for the full lesson on
&ldquo;{lesson_title}&rdquo; from <em>{module_title}</em>. The finished lesson
will run to around 800 words in plain English; this version exists so the
reading experience, progress tracking and content structure can be built and
tested first.</p>

<h2>What this lesson will cover</h2>
<ul>
  <li>The one idea that matters most, stated plainly.</li>
  <li>A real Australian example you'll recognise.</li>
  <li>The single habit that prevents most problems.</li>
</ul>

<h3>A worked example</h3>
<p>The real lesson walks through a situation you might actually meet at work,
step by step, and points out exactly where the risk is and what to do about it.</p>

<blockquote>Key point: you don't need to be technical to stay safe — you need to
know what to look for, and to slow down when something feels rushed.</blockquote>

<h3>Quick reference</h3>
<table>
  <thead><tr><th>If you see&hellip;</th><th>Do this</th></tr></thead>
  <tbody>
    <tr><td>An unexpected urgent request</td><td>Stop and verify another way.</td></tr>
    <tr><td>A link you weren't expecting</td><td>Don't click — check the address first.</td></tr>
  </tbody>
</table>

<p>The full lesson ends with a short recap and leads into the next one.</p>
""".strip()


# --- Scene-based branching simulations (Modules 1 and 2) -------------------
# A visual, scene-by-scene story: each scene has a backdrop illustration (styled
# by cybaroo.css from `backdrop`), a narrative, and choices. Picking one reveals
# its consequence, then Continue advances to the next scene, ending in a summary.
# cybaroo.js drives it and posts score/total/path to complete_simulation.

MODULE1_SIM = {
    "kind": "scenes",
    "intro": "You look after the network at Wattle Grove Medical Centre, a busy "
    "Bendigo clinic. Two things need your attention this morning. Read what is "
    "actually on each screen, then make the call, using what Lesson 1 taught about "
    "weak points and who is on your Wi-Fi.",
    "start": "router",
    "scenes": {
        "router": {
            "backdrop": "win",
            "screen": {
                "chrome": "browser",
                "tab": "Router admin",
                "secure": False,
                "url": "192.168.0.1/settings/security",
                "rows": [
                    {"k": "Admin password", "v": "admin", "flag": "bad"},
                    {"k": "Wi-Fi encryption", "v": "WPA2 (on)", "flag": "ok"},
                    {"k": "Guest network", "v": "On · Open, no password", "flag": "warn"},
                    {"k": "Firmware", "v": "Up to date", "flag": "ok"},
                ],
            },
            "title": "9:05am, the router settings page is open",
            "narrative": "You have logged in to the clinic router to check it over. "
            "Read the four settings above. Three are fine, but one is a wide-open "
            "door that Lesson 1 called the single most important fix. Which do you "
            "deal with first?",
            "choices": [
                {"label": "Change the admin password, still set to the factory default 'admin'",
                 "outcome": "good", "to": "devices",
                 "consequence": "Right. Default router passwords like 'admin' are "
                 "printed in manuals and listed online, so anyone who reaches the "
                 "page can log in and change anything. Setting a long, unique "
                 "password is the single most important fix. The open guest network "
                 "is worth a look next, but the default admin password is the "
                 "wide-open front door."},
                {"label": "Turn off WPA2, since encryption seems to be slowing the Wi-Fi",
                 "outcome": "bad", "to": "devices",
                 "consequence": "That removes the very protection keeping your "
                 "wireless traffic private, and it has nothing to do with speed. "
                 "WPA2 is a good setting. The real problem on this page is the admin "
                 "password still set to the factory default 'admin'."},
                {"label": "Nothing needs changing; up-to-date firmware means it is secure",
                 "outcome": "bad", "to": "devices",
                 "consequence": "Up-to-date firmware is good, but it does not make up "
                 "for a default password. Anyone who reaches this page can log in "
                 "with 'admin' and take over the router. Change that password "
                 "first."},
            ],
        },
        "devices": {
            "backdrop": "win",
            "screen": {
                "chrome": "window",
                "icon": "i-shield",
                "title": "Clinic Wi-Fi · Connected devices",
                "items": [
                    {"name": "Reception iPad", "sub": "192.168.1.12 · joined 9:01am", "tag": "This clinic"},
                    {"name": "Dr Chen's Laptop", "sub": "192.168.1.14 · joined 8:32am", "tag": "This clinic"},
                    {"name": "Clinic Printer", "sub": "192.168.1.30 · always on", "tag": "This clinic"},
                    {"name": "UNKNOWN DEVICE", "sub": "4f:2a:9c:81:e0 · joined 2 hours ago", "tag": "Not recognised", "flag": "bad"},
                ],
            },
            "title": "11:20am, the connected-devices list",
            "narrative": "You open the list of everything on the clinic Wi-Fi. Three "
            "devices are the clinic's own. One, with an unfamiliar hardware address, "
            "joined two hours ago and is not recognised. What do you do?",
            "choices": [
                {"label": "Change the Wi-Fi password so unknown devices drop off, then set up a guest network",
                 "outcome": "good", "to": "end",
                 "consequence": "Exactly. Changing the Wi-Fi password forces every "
                 "device to reconnect with the new one, so anything you did not "
                 "authorise simply falls off. A separate guest network then keeps "
                 "visitors' phones away from the computers holding patient records "
                 "for good."},
                {"label": "Leave it; it is probably a patient's phone that found the password",
                 "outcome": "bad", "to": "end",
                 "consequence": "Maybe, but you cannot assume that. An unrecognised "
                 "device sharing the same network as your patient records is worth "
                 "two minutes to shut out. Change the Wi-Fi password so it drops "
                 "off."},
                {"label": "Unplug the router for the rest of the day to be safe",
                 "outcome": "bad", "to": "end",
                 "consequence": "That takes the whole clinic offline, staff and all, "
                 "for one unknown device, and it can simply reconnect when the "
                 "router comes back. Change the Wi-Fi password instead of pulling "
                 "the plug."},
            ],
        },
        "end": {
            "backdrop": "win",
            "title": "That is the clinic network looked after",
            "narrative": "Two ordinary checks, one steady habit behind both: read "
            "what the screen is actually telling you, close the door you did not "
            "mean to leave open, and keep the people you do not know off the "
            "systems that hold what matters. That is what looking after a network "
            "really means.",
        },
    },
}

MODULE2_SIM = {
    "kind": "scenes",
    "intro": "It is a normal Tuesday at Corangamite Accounting, a small firm in "
    "Colac, until the shared drive starts behaving strangely. Read what is on each "
    "screen, then make the call, using what Lesson 1 taught about ransomware.",
    "start": "files",
    "scenes": {
        "files": {
            "backdrop": "win",
            "screen": {
                "chrome": "window", "icon": "i-lock",
                "title": "File Explorer", "menu": "This PC › Shared › Clients",
                "items": [
                    {"name": "Nguyen_BAS_2026.xlsx.locked", "sub": "LOCKED File · 2:00pm", "tag": "Locked", "flag": "bad"},
                    {"name": "Patel_tax_return.pdf.locked", "sub": "LOCKED File · 2:00pm", "tag": "Locked", "flag": "bad"},
                    {"name": "payroll_march.csv.locked", "sub": "LOCKED File · 2:01pm", "tag": "Locked", "flag": "bad"},
                    {"name": "READ_ME_TO_UNLOCK.txt", "sub": "Text · added 2:01pm", "tag": "Ransom note", "flag": "bad"},
                ],
            },
            "title": "2:03pm, the shared drive looks wrong",
            "narrative": "Every file on the Clients folder has been renamed to end "
            ".locked, and a file called READ_ME_TO_UNLOCK has appeared. A colleague "
            "two desks over says their files just stopped opening too. What is your "
            "first move?",
            "choices": [
                {"label": "Disconnect the affected computers from the network, then report it",
                 "outcome": "good", "to": "backup",
                 "consequence": "Right. Getting the machines off the network first "
                 "stops the ransomware reaching more of the shared drive and other "
                 "computers, and reporting it brings the right help fast. Contain, "
                 "then report, then recover."},
                {"label": "Open READ_ME_TO_UNLOCK and pay the demand to get the files back",
                 "outcome": "bad", "to": "backup",
                 "consequence": "Paying is unreliable, funds more crime, and leaves "
                 "the way in open so it can happen again. And while you read the note, "
                 "the encryption keeps spreading. Disconnect and contain first."},
                {"label": "Tell everyone to keep working so no unsaved work is lost",
                 "outcome": "bad", "to": "backup",
                 "consequence": "Every second the machines stay connected, more files "
                 "and more computers are locked. A little unsaved work is nothing "
                 "against the whole drive. The first move is to disconnect."},
            ],
        },
        "backup": {
            "backdrop": "win",
            "screen": {
                "chrome": "window", "icon": "i-shield",
                "title": "Backup console", "menu": "Backups › Nightly",
                "rows": [
                    {"k": "Last backup", "v": "Last night, 2:00am", "flag": "ok"},
                    {"k": "Integrity", "v": "Verified", "flag": "ok"},
                    {"k": "Location", "v": "Offline copy, kept off the network", "flag": "ok"},
                    {"k": "Ransom demand", "v": "0.05 BTC · 72h countdown", "flag": "bad"},
                ],
            },
            "title": "The machines are contained. Now recover.",
            "narrative": "IT has checked the backup console. Last night's backup is "
            "complete, verified, and was kept on an offline copy the ransomware could "
            "not reach. The ransom note still demands payment. How do you get back to "
            "work?",
            "choices": [
                {"label": "Wipe the affected machines and restore from the clean, verified backup",
                 "outcome": "good", "to": "end",
                 "consequence": "Exactly. A tested, offline backup is what takes away "
                 "the attacker's power entirely. You rebuild the machines, restore the "
                 "files, and pay nothing. That is how a business beats ransomware."},
                {"label": "Pay the 0.05 BTC anyway, to be quick",
                 "outcome": "bad", "to": "end",
                 "consequence": "With a clean backup in hand, paying makes no sense at "
                 "all. It rewards the attacker and there is no guarantee the files come "
                 "back. Restore from the backup instead."},
                {"label": "Reconnect an infected machine to check if the files came back",
                 "outcome": "bad", "to": "end",
                 "consequence": "Reconnecting an infected machine can spread the "
                 "ransomware all over again. Keep the infected machines isolated, wipe "
                 "them, and restore from the clean backup."},
            ],
        },
        "end": {
            "backdrop": "win",
            "title": "That is the incident handled",
            "narrative": "You recognised ransomware the moment the files changed, "
            "contained it before it spread further, and recovered from a clean backup "
            "without paying a cent. Contain, report, restore: that steady order is "
            "what keeps a small business standing.",
        },
    },
}

MODULE3_SIM = {
    "kind": "scenes",
    "intro": "You are on the front desk at Brunswick Family Dental. Two messages "
    "this afternoon both want money moved. Read exactly what is on each screen, then "
    "decide, using what Lesson 1 taught about business email compromise and voice "
    "clones.",
    "start": "email",
    "scenes": {
        "email": {
            "backdrop": "email",
            "screen": {
                "chrome": "browser", "tab": "Mail · Inbox", "secure": True,
                "url": "mail.brunswickfamilydental.com.au/inbox",
                "email": {
                    "from": "Dr Priya Lam <p.lam@dental-admin-mail.com>",
                    "subject": "URGENT: confidential payment needed today",
                    "date": "2:11pm",
                    "preview": "I'm between patients and can't take calls. Please pay "
                    "our new dental lab $48,500 before 4pm today, and keep this "
                    "between us for now. I'll explain later. Thanks, Priya.",
                },
            },
            "title": "2:11pm, an urgent email from Dr Lam",
            "narrative": "It looks like it is from the principal, Dr Lam. Read the "
            "sender address after the name, and the request itself: an unusual "
            "payment, a deadline, and a request to keep it quiet. What do you do?",
            "choices": [
                {"label": "Call Dr Lam on the number you already have and confirm before doing anything",
                 "outcome": "good", "to": "call",
                 "consequence": "Right. The address is a lookalike (dental-admin-mail.com, "
                 "not the practice's domain), and the pressure and secrecy are there to "
                 "stop you checking. Verifying on a number you already trust is the one "
                 "move this scam cannot survive."},
                {"label": "Pay the $48,500 to the new dental lab, since it is from Dr Lam",
                 "outcome": "bad", "to": "call",
                 "consequence": "That is exactly what business email compromise relies "
                 "on. The lookalike domain, the urgency, and the secrecy are all red "
                 "flags. Any new or urgent payment deserves a call to a trusted number "
                 "first."},
                {"label": "Reply to the email asking Dr Lam to confirm the account",
                 "outcome": "bad", "to": "call",
                 "consequence": "If the mailbox is impersonated or compromised, your "
                 "question goes to the attacker, who happily confirms. Replying can "
                 "never verify a suspicious message. Use a channel you already trust."},
            ],
        },
        "call": {
            "backdrop": "phone",
            "screen": {
                "chrome": "phone", "time": "2:14pm", "app": "Incoming call",
                "rows": [
                    {"k": "Caller", "v": "Dr Priya Lam (principal)"},
                    {"k": "Number", "v": "+61 4●● ●●● 118"},
                    {"k": "Note", "v": "Saved in your contacts", "flag": "warn"},
                ],
            },
            "title": "2:14pm, the front desk phone rings",
            "narrative": "The caller ID shows Dr Lam's name and number, and the voice "
            "on the line sounds exactly like her. She is insistent: make the transfer "
            "now, and why are you asking questions? What do you do?",
            "choices": [
                {"label": "Hang up and call Dr Lam back on the number saved from before, not this call",
                 "outcome": "good", "to": "end",
                 "consequence": "Exactly. A caller ID can be spoofed and a voice can be "
                 "cloned from a few seconds of public audio. Calling back on a number "
                 "you already trust is the one check neither trick can beat."},
                {"label": "Make the transfer; the voice is clearly Dr Lam",
                 "outcome": "bad", "to": "end",
                 "consequence": "A familiar voice is no longer proof. AI voice cloning "
                 "can copy a person from a short clip. Never move money on a voice and "
                 "a caller ID alone."},
                {"label": "Ask a personal question to check it is really her",
                 "outcome": "bad", "to": "end",
                 "consequence": "A well-prepared attacker may know the answer, and a "
                 "clone can respond smoothly. Do not try to out-quiz the caller. Hang "
                 "up and call back on a trusted number."},
            ],
        },
        "end": {
            "backdrop": "win",
            "title": "Nothing paid, everyone warned",
            "narrative": "Two convincing approaches, one steady habit: do not act on "
            "the message in front of you, verify through a channel you already trust, "
            "and report it so the next person is ready. That is reading a con like an "
            "analyst.",
        },
    },
}

MODULE4_SIM = {
    "kind": "scenes",
    "intro": "You look after admin at Kensington Physiotherapy and you are working "
    "from a cafe today. Two everyday moments, each with a safer and a riskier "
    "path. Read the screen, then choose, using what Lesson 1 taught about secure "
    "sending and untrusted Wi-Fi.",
    "start": "send",
    "scenes": {
        "send": {
            "backdrop": "email",
            "screen": {
                "chrome": "window", "icon": "i-mail", "title": "New message",
                "rows": [
                    {"k": "To", "v": "joe.private@gmail.com", "flag": "warn"},
                    {"k": "Subject", "v": "the form"},
                    {"k": "Attached", "v": "Nguyen_medical_history.pdf", "flag": "warn"},
                    {"k": "Encryption", "v": "None (ordinary email)", "flag": "bad"},
                ],
            },
            "title": "10:40am, about to send a patient's medical history",
            "narrative": "A colleague has asked you to send a patient's medical "
            "history to their personal Gmail, as a plain attachment, so they can read "
            "it at home. It is highly sensitive health data. What do you do?",
            "choices": [
                {"label": "Stop, and send it through the clinic's secure portal, or password-protect it and send the password separately",
                 "outcome": "good", "to": "wifi",
                 "consequence": "Right. Health data is exactly what needs a sealed "
                 "channel, so only the intended person can open it and one wrong "
                 "address is not a breach. If you password-protect the file, send the "
                 "password by a different channel, never in the same email."},
                {"label": "Send it as-is; plain email is quicker and the colleague is waiting",
                 "outcome": "bad", "to": "wifi",
                 "consequence": "Plain email is a postcard, and a personal Gmail is "
                 "outside the clinic's control. One wrong address, or anyone along the "
                 "way, and sensitive health data is exposed. Use a sealed channel."},
                {"label": "Send it, but CC your manager so there is a second copy",
                 "outcome": "bad", "to": "wifi",
                 "consequence": "That just exposes the private file to more inboxes. "
                 "The fix is a sealed, access-controlled channel, not more copies of an "
                 "unprotected one."},
            ],
        },
        "wifi": {
            "backdrop": "wifi",
            "screen": {
                "chrome": "phone", "time": "10:52am", "app": "Wi-Fi",
                "items": [
                    {"name": "Corner Cafe Free WiFi", "sub": "Open · no password", "tag": "Open", "flag": "bad"},
                    {"name": "Corner Cafe Free WiFi", "sub": "Open · no password", "tag": "Open", "flag": "bad"},
                    {"name": "TelstraAir", "sub": "Secured", "tag": "Secured"},
                ],
            },
            "title": "10:52am, time to get online",
            "narrative": "You need to reach the clinic system. The cafe Wi-Fi list "
            "shows two networks with exactly the same name, both open, and one "
            "secured network. One of the identical two may be an evil twin. How do "
            "you connect?",
            "choices": [
                {"label": "Use your phone's mobile data, or a VPN, rather than any open cafe network",
                 "outcome": "good", "to": "end",
                 "consequence": "Right. Two identical open networks is a classic "
                 "evil-twin setup: connect to the wrong one and everything you send "
                 "runs through an attacker. Your own mobile data is encrypted and "
                 "yours; a VPN protects you even on untrusted Wi-Fi."},
                {"label": "Join the first 'Corner Cafe Free WiFi' in the list",
                 "outcome": "bad", "to": "end",
                 "consequence": "You cannot tell the real cafe network from a "
                 "lookalike by name alone, and an open network carries your traffic in "
                 "the clear anyway. Use mobile data or a VPN instead."},
                {"label": "Join the other 'Corner Cafe Free WiFi', it has a stronger signal",
                 "outcome": "bad", "to": "end",
                 "consequence": "A strong signal often means the attacker's hotspot is "
                 "closest to you. Signal strength proves nothing. Do not trust either "
                 "open network; use mobile data or a VPN."},
            ],
        },
        "end": {
            "backdrop": "win",
            "title": "Sent safely, connected safely",
            "narrative": "Match the care to the sensitivity, and never trust a "
            "network you do not control. Sealed channels for private data, and your "
            "own connection or a VPN when you are out: two habits that keep client "
            "information where it belongs.",
        },
    },
}

MODULE5_SIM = {
    "kind": "scenes",
    "intro": "You help run IT for Yarra Freight, a Melbourne logistics firm. Two "
    "requests land on your desk this week. Read what each screen shows, then decide, "
    "using what Lesson 1 taught about firewalls, remote access, and keeping things "
    "patched.",
    "start": "remote",
    "scenes": {
        "remote": {
            "backdrop": "win",
            "screen": {
                "chrome": "window", "icon": "i-shield",
                "title": "Firewall · Rules", "menu": "Security › Rules (top-down)",
                "rows": [
                    {"k": "1  ALLOW", "v": "Staff → internet (web, email)", "flag": "ok"},
                    {"k": "2  ALLOW", "v": "Office → payment gateway", "flag": "ok"},
                    {"k": "3  DENY", "v": "Everything else (default-deny)", "flag": "ok"},
                    {"k": "Pending", "v": "Open Remote Desktop to the internet?", "flag": "warn"},
                ],
            },
            "title": "Monday, a request to allow working from home",
            "narrative": "A manager wants to work from home and asks you to 'just "
            "open Remote Desktop to the internet' so they can log in. The firewall "
            "is currently default-deny. What do you do?",
            "choices": [
                {"label": "Say no; set up a VPN with multi-factor sign-in so the office systems stay hidden",
                 "outcome": "good", "to": "patch",
                 "consequence": "Right. Remote Desktop exposed to the internet is one "
                 "of the most common ways attackers and ransomware get in: automated "
                 "scanners find it within hours and hammer the login. A VPN with "
                 "multi-factor is one guarded door, and the office systems stay out of "
                 "sight."},
                {"label": "Add a rule opening Remote Desktop to the internet",
                 "outcome": "bad", "to": "patch",
                 "consequence": "That punches a hole straight through your default-deny "
                 "firewall to a login attackers scan for constantly. This is exactly "
                 "how the Medibank-style break-ins begin. Use a VPN with multi-factor "
                 "instead."},
                {"label": "Open it for one week only, then close it",
                 "outcome": "bad", "to": "patch",
                 "consequence": "A week is more than enough for automated scanners to "
                 "find the open port and start guessing passwords, and 'temporary' "
                 "rules are famous for staying open. Set up the VPN properly."},
            ],
        },
        "patch": {
            "backdrop": "win",
            "screen": {
                "chrome": "window", "icon": "i-shield",
                "title": "Security dashboard", "menu": "Overview",
                "rows": [
                    {"k": "VPN", "v": "On · multi-factor required", "flag": "ok"},
                    {"k": "Firewall", "v": "Default-deny", "flag": "ok"},
                    {"k": "Guest Wi-Fi", "v": "Separate zone", "flag": "ok"},
                    {"k": "Updates", "v": "3 servers overdue by 40 days", "flag": "bad"},
                ],
            },
            "title": "The dashboard shows one thing outstanding",
            "narrative": "The remote access is sorted. The security dashboard is "
            "mostly green, but three servers are 40 days behind on updates. What do "
            "you do?",
            "choices": [
                {"label": "Schedule and apply the overdue updates now",
                 "outcome": "good", "to": "end",
                 "consequence": "Right. Most break-ins use a hole a patch had already "
                 "fixed. A firewall cannot save a server with a known, unpatched flaw. "
                 "Applying updates promptly is a core part of defence in depth."},
                {"label": "Ignore them; the firewall will keep the servers safe",
                 "outcome": "bad", "to": "end",
                 "consequence": "A firewall controls which connections are allowed; it "
                 "does not fix a known flaw in a service you do allow. Defence in depth "
                 "means the updates matter too. Patch them."},
                {"label": "Turn off automatic updates so they stop nagging",
                 "outcome": "bad", "to": "end",
                 "consequence": "That is the opposite of the fix. Turning updates off "
                 "leaves every known hole wide open. Apply the overdue ones and keep "
                 "automatic updates on."},
            ],
        },
        "end": {
            "backdrop": "win",
            "title": "The defences are holding",
            "narrative": "One guarded, encrypted door instead of many exposed to the "
            "internet, and every layer kept up to date. A firewall is one wall; real "
            "security is layers, each covering what the others cannot."},
    },
}

MODULE6_SIM = {
    "kind": "scenes",
    "intro": "You are the office manager at Riverside Dental in Geelong when the "
    "monitoring board lights up. Read what each screen tells you, then make the "
    "call, using the response steps and the law from Lesson 1.",
    "start": "alert",
    "scenes": {
        "alert": {
            "backdrop": "win",
            "screen": {
                "chrome": "window", "icon": "i-shield",
                "title": "Monitoring · Alerts", "menu": "Live › Today",
                "rows": [
                    {"k": "09:14", "v": "Many failed logins, then one success", "flag": "bad"},
                    {"k": "09:20", "v": "Files encrypting on the records server", "flag": "bad"},
                    {"k": "Patient records", "v": "At risk", "flag": "bad"},
                    {"k": "Backups", "v": "Last night, verified, offline", "flag": "ok"},
                ],
            },
            "title": "09:22, the alert board lights up",
            "narrative": "The monitoring board shows a break-in an hour ago and files "
            "now encrypting on the patient-records server. Staff are asking what to "
            "do. What is your first move?",
            "choices": [
                {"label": "Isolate the affected machines from the network, then start the response plan and report it",
                 "outcome": "good", "to": "notify",
                 "consequence": "Right. Disconnecting the affected machines contains "
                 "the spread without destroying the evidence a full power-off would "
                 "lose, and starting the plan brings the right people in. Contain "
                 "first, then work through the phases in order."},
                {"label": "Pull the power on every machine at the wall, immediately",
                 "outcome": "bad", "to": "notify",
                 "consequence": "A blind power-off can destroy useful evidence, may not "
                 "stop the spread, and knocks out systems you did not need to lose. "
                 "Isolate the affected machines from the network instead."},
                {"label": "Wait to see if it stops before worrying anyone",
                 "outcome": "bad", "to": "notify",
                 "consequence": "Waiting is the most expensive choice in an incident. "
                 "Every minute, more records are encrypted and the break-in spreads. "
                 "Name it as an incident and contain it now."},
            ],
        },
        "notify": {
            "backdrop": "leak",
            "screen": {
                "chrome": "window", "icon": "i-book",
                "title": "Privacy · Breach assessment", "menu": "Notifiable Data Breaches",
                "rows": [
                    {"k": "Data exposed", "v": "Patient health records", "flag": "bad"},
                    {"k": "Serious harm", "v": "Likely", "flag": "bad"},
                    {"k": "Assess within", "v": "30 days", "flag": "warn"},
                    {"k": "Regulator", "v": "OAIC", "flag": "warn"},
                ],
            },
            "title": "Contained and recovered. Now the law.",
            "narrative": "The machines are isolated, and clean backups are restoring "
            "the records. But patient health data was copied before the encryption. "
            "Under the Notifiable Data Breaches scheme, what do you do?",
            "choices": [
                {"label": "Notify the OAIC and the affected patients, and tell them how to protect themselves",
                 "outcome": "good", "to": "end",
                 "consequence": "Right. Exposed health data is very likely to cause "
                 "serious harm, so the Privacy Act requires notifying the OAIC and the "
                 "affected people as soon as practicable. Telling people promptly is "
                 "the law, and it lets them protect themselves."},
                {"label": "Keep it quiet to avoid embarrassing the practice",
                 "outcome": "bad", "to": "end",
                 "consequence": "Staying quiet about an eligible breach of health data "
                 "breaks the law and leaves patients unable to protect themselves. The "
                 "scheme exists precisely so people are told."},
                {"label": "Wait several months and decide later",
                 "outcome": "bad", "to": "end",
                 "consequence": "The scheme runs on a clock: you must assess a "
                 "suspected eligible breach within 30 days and notify as soon as "
                 "practicable. Drifting for months is not an option."},
            ],
        },
        "end": {
            "backdrop": "win",
            "title": "Handled, start to finish",
            "narrative": "You named the incident fast, contained it before it spread, "
            "recovered from clean backups, and met the practice's legal duty to the "
            "people whose data was exposed. Panic is optional; a plan is not."},
    },
}

MODULE_SIMS = {1: MODULE1_SIM, 2: MODULE2_SIM, 3: MODULE3_SIM, 4: MODULE4_SIM,
               5: MODULE5_SIM, 6: MODULE6_SIM}


def _placeholder_sim(module_title):
    return {
        "kind": "inbox",
        "intro": f"A short interactive scenario for {module_title}. The full "
        "version will present realistic situations to judge. This placeholder "
        "keeps the same shape so the exercise runs end to end.",
        "items": [
            {
                "id": "safe",
                "from": "A trusted colleague",
                "subject": "A normal, expected request",
                "preview": "This message is exactly what it appears to be.",
                "scam": False,
                "tells": ["Expected, from someone you know, no pressure."],
            },
            {
                "id": "scam",
                "from": "An unfamiliar sender",
                "subject": "An urgent request you weren't expecting",
                "preview": "Act now or something bad happens — the usual pressure.",
                "scam": True,
                "tells": ["Unexpected, urgent, and pushing you to act fast."],
            },
        ],
    }


def _seed_lesson_tasks(lesson, tasks):
    """Seed a lesson's interactive tasks idempotently (keyed on task_key).

    Each activity carries its own `payload` config verbatim (sort/inbox/spot/
    password/branch); legacy check/scenario tasks build theirs from options.
    Tasks no longer present in the content are pruned, so re-running mirrors the
    content exactly.
    """
    from modules.models import sanitise_lesson_html

    def _options(pairs):
        return [
            {"text": text, "correct": correct, "explanation": explanation}
            for (text, correct, explanation) in pairs
        ]

    seen = []
    for order, t in enumerate(tasks, start=1):
        if t["kind"] in ("check", "scenario"):
            payload = {
                "question": t.get("question", ""),
                "scenario": t.get("scenario", ""),
                "hint": t.get("hint", ""),
                "options": _options(t["options"]),
            }
        else:
            payload = dict(t.get("payload", {}))
        # Optional mid-panel check and a second reading block, rendered between
        # the main body and the panel's end interactive. body2 is sanitised
        # (it is HTML rendered with |safe); the payload itself is not.
        if t.get("inline_check"):
            ic = t["inline_check"]
            payload["inline_check"] = {
                "question": ic.get("question", ""),
                "hint": ic.get("hint", ""),
                "options": _options(ic["options"]),
            }
        if t.get("body2"):
            payload["body2"] = sanitise_lesson_html(t["body2"])
        # Optional "hero" figure: a diagram partial rendered at the very top of
        # the panel as a visual anchor, above the panel's own diagram/body.
        if t.get("hero"):
            payload["hero"] = t["hero"]
        LessonTask.objects.update_or_create(
            lesson=lesson,
            task_key=t["key"],
            defaults={
                "order": order,
                "kind": t["kind"].upper(),
                "points": t["points"] * _POINTS_SCALE,
                "title": t.get("title", ""),
                "body": t.get("body", ""),
                "diagram_key": t.get("diagram", ""),
                "payload": payload,
                "image": t.get("image", {}),
            },
        )
        seen.append(t["key"])
    lesson.tasks.exclude(task_key__in=seen).delete()


def _seed_module_quiz(module, content, lessons_by_number, force=False):
    """Seed a module's real quiz and its question bank, idempotently.

    Questions key on (quiz, ordering) and options on (question, option_text). When
    content is revised, stale rows are pruned: options no longer in a question and
    questions beyond the current bank are removed, so re-running mirrors the
    content exactly rather than leaving a question with two "correct" options.
    Every option carries an explanation, the Adaptive Feedback Engine's fuel.

    A question an admin has edited in the console (admin_edited=True) is left
    exactly as they left it — question row AND its answers — unless the seed is
    run with --force. This is how a reseed can't silently wipe an admin's edit.
    """
    quiz_data = content.QUIZ
    quiz, _ = Quiz.objects.update_or_create(
        module=module,
        defaults={
            "pass_mark": quiz_data["pass_mark"],
            "is_active": True,
            "time_limit_minutes": 30,
        },
    )
    for ordering, q in enumerate(quiz_data["questions"], start=1):
        question, created = Question.objects.get_or_create(
            quiz=quiz,
            ordering=ordering,
            defaults={
                "question_text": q["text"],
                "difficulty": q["difficulty"],
                "lesson_reference": lessons_by_number[q["lesson"]],
            },
        )
        # Admin-locked question: leave it and its answers untouched.
        if not created and question.admin_edited and not force:
            continue
        if not created:
            question.question_text = q["text"]
            question.difficulty = q["difficulty"]
            question.lesson_reference = lessons_by_number[q["lesson"]]
            if force:
                question.admin_edited = False
            question.save()
        current_texts = []
        for option_text, is_correct, explanation in q["options"]:
            Answer.objects.update_or_create(
                question=question,
                option_text=option_text,
                defaults={
                    "correct_answer": is_correct,
                    "explanation_text": explanation,
                },
            )
            current_texts.append(option_text)
        # Drop options left over from an earlier version of this question.
        question.answers.exclude(option_text__in=current_texts).delete()
    # Drop questions beyond the current bank size.
    quiz.questions.filter(ordering__gt=len(quiz_data["questions"])).delete()
    return quiz


class Command(BaseCommand):
    help = "Create/refresh the six training modules, their lessons and simulations."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Overwrite content even where an admin has edited it in the "
            "console (admin_edited=True), and clear that flag. Use this to reset "
            "content back to the authored source in modules/content/. Without it, "
            "admin-edited modules, lessons and questions are left untouched.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        force = options["force"]
        author = (
            User.objects.filter(is_superuser=True).order_by("pk").first()
            or User.objects.order_by("pk").first()
        )
        if author is None:
            raise CommandError(
                "No users exist to own the content. Create a superuser first: "
                "manage.py createsuperuser"
            )

        for index, (title, desc, difficulty, lesson_titles) in enumerate(MODULES, start=1):
            module, created = Module.objects.get_or_create(
                order_index=index,
                defaults={
                    "title": title,
                    "tagline": TAGLINES.get(index, ""),
                    "description": desc,
                    "difficulty": difficulty,
                    "is_published": True,
                    "created_by": author,
                    "duration_minutes": 40,
                },
            )
            # Refresh content on an existing module unless an admin has edited it
            # in the console. Publish state (is_published) is deliberately set
            # only on create, so an admin's publish/unpublish also survives a
            # reseed.
            if not created and (force or not module.admin_edited):
                module.title = title
                module.tagline = TAGLINES.get(index, "")
                module.description = desc
                module.difficulty = difficulty
                module.duration_minutes = 40
                if force:
                    module.admin_edited = False
                module.save()

            # Registered modules ship with real, finished lesson content; the
            # rest carry the rich placeholder until their turn.
            content = CONTENT.get(index)
            real_lessons = content.LESSONS if content else None
            lessons_by_number = {}
            for n, lesson_title in enumerate(lesson_titles, start=1):
                if real_lessons:
                    spec = real_lessons[n - 1]
                    # Task-based lesson: body_text is just a short intro; the
                    # teaching lives in the interactive tasks.
                    lesson_defaults = {
                        "title": spec["title"],
                        "body_text": f"<p>{spec['intro']}</p>",
                        "reading_time_minutes": spec["reading_time_minutes"],
                        "is_active": True,
                    }
                else:
                    lesson_defaults = {
                        "title": lesson_title,
                        "body_text": _placeholder_body(title, lesson_title),
                        "reading_time_minutes": 8,
                        "is_active": True,
                    }
                lesson, lesson_created = Lesson.objects.get_or_create(
                    module=module, lesson_number=n, defaults=lesson_defaults
                )
                # Refresh an existing lesson's content unless an admin edited it.
                # is_active is set only on create, so a lesson-level publish/
                # unpublish also survives a reseed.
                if not lesson_created and (force or not lesson.admin_edited):
                    lesson.title = lesson_defaults["title"]
                    lesson.body_text = lesson_defaults["body_text"]
                    lesson.reading_time_minutes = lesson_defaults["reading_time_minutes"]
                    if force:
                        lesson.admin_edited = False
                    lesson.save()
                # Interactive tasks are code-authored (not editable in the
                # console), so they always mirror the content file.
                if real_lessons:
                    _seed_lesson_tasks(lesson, spec["tasks"])
                lessons_by_number[n] = lesson

            sim_data = MODULE_SIMS.get(index) or _placeholder_sim(title)
            Simulation.objects.update_or_create(
                module=module,
                defaults={
                    "scenario_text": sim_data["intro"],
                    "decision_points": sim_data,
                    "outcome_text": {},
                },
            )

            n_lessons = len(lesson_titles)
            if content:
                quiz = _seed_module_quiz(module, content, lessons_by_number, force=force)
                # Now that every question points at an authored lesson (1..n), any
                # lesson rows beyond the authored count are unreferenced and safe to
                # prune, so a reseed mirrors a module that deliberately ships fewer
                # lessons (for example Module 2's two deep lessons).
                module.lessons.filter(lesson_number__gt=n_lessons).delete()
                self.stdout.write(
                    f"  module {index}: {title}  ({n_lessons} lessons, 1 simulation, "
                    f"quiz with {quiz.questions.count()} questions)"
                )
            else:
                self.stdout.write(
                    f"  module {index}: {title}  ({n_lessons} lessons, 1 simulation)"
                )

        total_lessons = sum(len(lesson_titles) for *_, lesson_titles in MODULES)
        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {len(MODULES)} modules, "
                f"{total_lessons} lessons, {len(MODULES)} simulations, "
                f"and {len(CONTENT)} interactive quizzes."
            )
        )
