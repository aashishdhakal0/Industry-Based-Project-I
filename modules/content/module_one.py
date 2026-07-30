"""Module 1 — Network Security Fundamentals: interactive activities and the quiz.

Content, not schema: kept as plain data so it reads like the teaching material it
is, and so the seed command stays re-runnable. Written in plain Australian
English for non-technical readers — small businesses, councils, schools.

Each lesson is mostly DOING, not reading. A short CONCEPT intro sets up the idea,
then interactive activities carry the weight — sort, inbox, spot-the-fake,
password builder, branching scenario. Every task carries points; a lesson's tasks
sum to 10 (POINTS_PER_LESSON), so finishing the last banks the lesson through the
normal points path — the economy is unchanged, the activities fill an XP bar.

QUIZ is the end-of-module assessment (a 15-question bank; ten drawn per attempt).
Every option carries an explanation_text — the Adaptive Feedback Engine reads it
back to the learner, so wrong options explain the misconception, not just "no".
"""

# --------------------------------------------------------------------------
# Lessons — mostly interactive activities; each lesson's points sum to 10.
#   concept  — a short teaching intro (optional diagram); "continue" to finish
#   sort     — tap items into buckets; solved when all placed correctly
#   inbox    — inspect an email, click the suspicious parts; solved when all found
#   spot     — two things shown, tap the fake; solved on the correct pick
#   password — live strength meter; solved when a strong password is built
#   branch   — a clickable scenario; solved on reaching an ending
# Activity config lives in each task's `payload` (see the seed + activities.js).
# --------------------------------------------------------------------------

LESSONS = [
    {
        "title": "What a network is, and what we protect",
        "reading_time_minutes": 4,
        "intro": "Meet the thing we're protecting — then sort real situations "
        "onto the three pillars of security yourself.",
        "tasks": [
            {
                "key": "net-and-cia",
                "kind": "concept",
                "points": 2,
                "title": "Networks, and the three questions security asks",
                "diagram": "cia-triad",
                "body": "<p>A <strong>network</strong> is just devices connected to "
                "share information — your laptop, the office printer, the eftpos "
                "terminal, all talking through a router to the internet. Keeping it "
                "safe comes down to the <strong>CIA triad</strong> (nothing to do "
                "with spies) — the three things every security decision protects, "
                "shown here. Once they click, sort a few real situations yourself.</p>",
            },
            {
                "key": "cia-sort",
                "kind": "sort",
                "points": 8,
                "title": "Which pillar is at stake?",
                "payload": {
                    "prompt": "Tap each situation, then tap the pillar it's about. "
                    "Get all six right to finish.",
                    "buckets": [
                        {"id": "c", "label": "Confidentiality"},
                        {"id": "i", "label": "Integrity"},
                        {"id": "a", "label": "Availability"},
                    ],
                    "items": [
                        {"id": "list", "text": "A customer list is emailed to the wrong person",
                         "bucket": "c", "why": "The wrong person can now see it — confidentiality."},
                        {"id": "invoice", "text": "An invoice's bank details are secretly changed",
                         "bucket": "i", "why": "The data was altered without permission — integrity."},
                        {"id": "ransom", "text": "Ransomware locks all your files",
                         "bucket": "a", "why": "You can't reach your files — availability."},
                        {"id": "sticky", "text": "A password is left on a sticky note on the monitor",
                         "bucket": "c", "why": "It exposes access to the wrong eyes — confidentiality."},
                        {"id": "backup", "text": "A tested backup lets you restore after a crash",
                         "bucket": "a", "why": "It keeps information available — availability."},
                        {"id": "totals", "text": "A tampered spreadsheet shows the wrong totals",
                         "bucket": "i", "why": "The numbers were changed — integrity."},
                    ],
                },
            },
        ],
    },
    {
        "title": "Spotting the weak points",
        "reading_time_minutes": 5,
        "intro": "Attackers walk through open doors — a convincing email, a rushed "
        "moment. Inspect one yourself, then tell a real message from a scam.",
        "tasks": [
            {
                "key": "vectors-intro",
                "kind": "concept",
                "points": 2,
                "title": "The common ways in",
                "body": "<p>Most attacks aren't clever — they rely on a person having "
                "a busy day. The usual ways in are <strong>phishing</strong> "
                "(messages pretending to be someone you trust), weak or reused "
                "<strong>passwords</strong>, and <strong>out-of-date software</strong>. "
                "The biggest risk of all is ordinary <strong>human error</strong>, "
                "which is why attackers lean on <em>urgency</em> to stop you thinking. "
                "Let's practise slowing down and looking closely.</p>",
            },
            {
                "key": "phishing-inbox",
                "kind": "inbox",
                "points": 5,
                "title": "Inspect the email",
                "payload": {
                    "prompt": "This just landed in the shared inbox. Tap every part "
                    "that looks suspicious — find all the tells to finish.",
                    "avatar": "AP",
                    "parts": [
                        {"id": "from", "zone": "From",
                         "text": "AusPost Delivery <service@auspost-delivery.info>",
                         "bad": True,
                         "why": "Lookalike domain: auspost-delivery.info is NOT auspost.com.au."},
                        {"id": "subject", "zone": "Subject",
                         "text": "Parcel on hold — pay a $2.99 release fee within 24 hours",
                         "bad": True,
                         "why": "A small fee plus a tight deadline is a classic pressure tactic."},
                        {"id": "b1", "zone": "Body",
                         "text": "We attempted delivery but a small customs fee is outstanding.",
                         "bad": False,
                         "why": "On its own this is just context — the tells are the sender, the deadline and the link."},
                        {"id": "b2", "zone": "Body",
                         "text": "Pay now at http://auspost-delivery.info/pay or your parcel is returned.",
                         "bad": True,
                         "why": "An emailed payment link on a lookalike domain — never click; go to the real site yourself."},
                    ],
                },
            },
            {
                "key": "sms-spot",
                "kind": "spot",
                "points": 3,
                "title": "Which text is the scam?",
                "payload": {
                    "prompt": "Two texts about a parcel. Tap the fake one.",
                    "left": {
                        "sender": "AusPost",
                        "text": "Your parcel S12 3456 will arrive today 9am–1pm. "
                        "Track at auspost.com.au/track",
                    },
                    "right": {
                        "sender": "+61 4xx xxx",
                        "text": "AUSPOST: your parcel is held. Pay the $1.99 redelivery "
                        "fee now at aus-post-redelivery.co/pay",
                    },
                    "fake": "right",
                    "why": "The fake uses a lookalike link (aus-post-redelivery.co, not "
                    "auspost.com.au), demands a fee, and pushes urgency. The genuine one "
                    "just gives a delivery window and the real address — no payment, no pressure.",
                },
            },
        ],
    },
    {
        "title": "Locking the front door",
        "reading_time_minutes": 5,
        "intro": "The router is the front door to everything. Build a password worth "
        "trusting, then sort the habits that keep it shut.",
        "tasks": [
            {
                "key": "router-intro",
                "kind": "concept",
                "points": 2,
                "title": "Your router is the front door",
                "body": "<p>Almost everything you do online passes through the "
                "<strong>router</strong> — the box that connects your workplace to "
                "the internet. Two things matter most: a strong <strong>admin "
                "password</strong> (the one that changes its settings — its factory "
                "default is published online), and modern <strong>Wi-Fi "
                "encryption</strong>. Let's build that password.</p>",
            },
            {
                "key": "password-builder",
                "kind": "password",
                "points": 4,
                "title": "Build a strong admin password",
                "payload": {
                    "prompt": "Type a password for the office router. Watch the meter "
                    "explain itself — reach Strong to finish.",
                    "target": "strong",
                    "common": ["password", "password1", "123456", "12345678", "qwerty",
                               "admin", "letmein", "welcome", "monkey", "iloveyou"],
                    "tips": [
                        "Longer beats complicated — aim for 12+ characters.",
                        "A few unrelated words are strong and easy to recall.",
                        "Never reuse a password that guards anything else.",
                    ],
                },
            },
            {
                "key": "wifi-sort",
                "kind": "sort",
                "points": 4,
                "title": "Safe or risky?",
                "payload": {
                    "prompt": "Sort each Wi-Fi habit into Safe or Risky. All six right to finish.",
                    "buckets": [
                        {"id": "safe", "label": "Safe"},
                        {"id": "risky", "label": "Risky"},
                    ],
                    "items": [
                        {"id": "wpa", "text": "Using WPA3 or WPA2 encryption", "bucket": "safe",
                         "why": "Modern encryption protects everyone on the network."},
                        {"id": "default", "text": "Leaving the router admin password as default",
                         "bucket": "risky", "why": "Default admin passwords are published online."},
                        {"id": "guest", "text": "A separate guest network for visitors", "bucket": "safe",
                         "why": "Keeps visitors' devices away from your work ones."},
                        {"id": "cafe", "text": "Banking over open café Wi-Fi", "bucket": "risky",
                         "why": "You can't trust a network you don't control."},
                        {"id": "updates", "text": "Turning on automatic updates", "bucket": "safe",
                         "why": "Patches close holes before attackers can use them."},
                        {"id": "wep", "text": "Sticking with old WEP encryption", "bucket": "risky",
                         "why": "WEP has been broken for years."},
                    ],
                },
            },
        ],
    },
    {
        "title": "A week at Docklands Dental",
        "reading_time_minutes": 4,
        "intro": "Put it all together. Make the calls a real small business faces — "
        "and see where each one leads.",
        "tasks": [
            {
                "key": "capstone-branch",
                "kind": "branch",
                "points": 10,
                "title": "You're running the front desk",
                "payload": {
                    "prompt": "It's a busy week. Choose what you'd actually do — you can "
                    "always see the better path.",
                    "start": "n1",
                    "nodes": {
                        "n1": {
                            "text": "Monday. An email from “accounts@your-supplier-au.info” says an "
                            "invoice is overdue and the bank account has changed — pay within the hour "
                            "or the service stops.",
                            "choices": [
                                {"label": "Pay it quickly so nothing gets cut off", "to": "n1bad",
                                 "outcome": "bad",
                                 "feedback": "Urgency plus a changed bank account is the classic invoice scam — the money's gone."},
                                {"label": "Ring the supplier on the number you already have", "to": "n2",
                                 "outcome": "good",
                                 "feedback": "Exactly — verify a change of details through a channel you already trust."},
                            ],
                        },
                        "n1bad": {
                            "text": "You paid. An hour later the real supplier phones, confused about a "
                            "payment they never received.",
                            "choices": [{"label": "See what would have worked", "to": "n2"}],
                        },
                        "n2": {
                            "text": "Wednesday. A colleague clicks a link in a “your password expires "
                            "today” email, types their password, then feels uneasy about it.",
                            "choices": [
                                {"label": "Tell them to say nothing so no one's in trouble", "to": "n2bad",
                                 "outcome": "bad",
                                 "feedback": "Staying quiet lets a small problem grow. Fast reporting is what limits the damage."},
                                {"label": "Report it to IT now and reset the password", "to": "n3",
                                 "outcome": "good",
                                 "feedback": "Right — quick reporting turns a near-miss into a non-event."},
                            ],
                        },
                        "n2bad": {
                            "text": "Two days later the mailbox is quietly emailing scams to all your patients.",
                            "choices": [{"label": "See the better path", "to": "n3"}],
                        },
                        "n3": {
                            "text": "Friday. Reviewing the week, which single habit would have prevented "
                            "the most harm?",
                            "choices": [
                                {"label": "Two-factor authentication on email", "to": "end",
                                 "outcome": "good",
                                 "feedback": "Yes — a stolen password alone wouldn't have been enough to get in."},
                                {"label": "A faster internet plan", "to": "n3",
                                 "outcome": "bad",
                                 "feedback": "Speed isn't security. Try again."},
                            ],
                        },
                        "end": {
                            "text": "That's a real week handled: verify before you pay, report fast, and "
                            "turn on two-factor. That's network security in practice — no jargon required.",
                            "choices": [],
                        },
                    },
                },
            },
        ],
    },
]


# --------------------------------------------------------------------------
# Quiz — a 15-question bank; ten drawn per attempt.
# Each question names the lesson it comes from (1-based, into LESSONS above) so
# the Adaptive Feedback Engine can trace a mistake back to the right lesson.
# Options: exactly one correct; every option carries an explanation.
# --------------------------------------------------------------------------

QUIZ = {
    "pass_mark": 70,
    "questions": [
        {
            "lesson": 1,
            "difficulty": "EASY",
            "text": "In plain terms, what is a computer network?",
            "options": [
                ("Two or more devices connected so they can share information", True,
                 "Correct — a network is just devices connected to share information, from two machines to the whole internet."),
                ("A single computer with a fast processor", False,
                 "No — one computer on its own isn't a network; a network is about devices being connected to each other."),
                ("A type of antivirus program", False,
                 "No — antivirus is software that protects a device; it isn't what a network is."),
                ("The password you use to log in", False,
                 "No — a password protects access, but it isn't the network itself."),
            ],
        },
        {
            "lesson": 1,
            "difficulty": "EASY",
            "text": "What do the letters in the 'CIA triad' stand for?",
            "options": [
                ("Confidentiality, Integrity and Availability", True,
                 "Correct — these are the three things security protects, and most decisions come back to one of them."),
                ("Computers, Internet and Applications", False,
                 "No — the triad is about what we protect, not a list of equipment."),
                ("Control, Inspection and Access", False,
                 "No — these sound plausible but aren't the triad; it's Confidentiality, Integrity and Availability."),
                ("Confidential Intelligence Agency", False,
                 "No — despite the initials, the CIA triad has nothing to do with spy agencies."),
            ],
        },
        {
            "lesson": 1,
            "difficulty": "MEDIUM",
            "text": "An invoice's bank details are secretly changed so payment goes to a stranger. Which part of the CIA triad has failed?",
            "options": [
                ("Integrity — the information was altered without permission", True,
                 "Correct — the file still opens, but its accuracy is gone; that's an integrity failure, and a common way money is stolen."),
                ("Availability — the file can't be opened", False,
                 "No — availability is about whether you can access something; here the file opens fine, it's just been tampered with."),
                ("Confidentiality — someone saw information they shouldn't", False,
                 "Not quite — the problem isn't who saw it, it's that the details were changed. That's integrity."),
                ("None of them — this isn't a security issue", False,
                 "No — altering financial details without permission is very much a security issue: a failure of integrity."),
            ],
        },
        {
            "lesson": 1,
            "difficulty": "MEDIUM",
            "text": "Keeping a restorable backup of your files mainly protects which part of the CIA triad?",
            "options": [
                ("Availability — you can still get your information when you need it", True,
                 "Correct — backups mean an attack or mistake doesn't cost you access to your information; that's availability."),
                ("Confidentiality — it hides the files from others", False,
                 "No — a backup doesn't hide anything; it ensures you can still get your data back. That's availability."),
                ("Integrity — it proves the files weren't changed", False,
                 "Not the main point — backups are chiefly about being able to restore access, which is availability."),
                ("Backups aren't related to security at all", False,
                 "No — backups are a core security control; they protect availability against ransomware and mistakes."),
            ],
        },
        {
            "lesson": 2,
            "difficulty": "EASY",
            "text": "What is 'phishing'?",
            "options": [
                ("A message pretending to be from someone you trust, to trick you into clicking or sharing details", True,
                 "Correct — phishing impersonates a trusted sender and is the most common way organisations are attacked."),
                ("A way of speeding up your internet connection", False,
                 "No — phishing has nothing to do with connection speed; it's a form of deception."),
                ("A tool that backs up your files", False,
                 "No — that's a backup; phishing is a scam message designed to trick you."),
                ("A setting on your router", False,
                 "No — phishing is a type of attack delivered by message, not a router setting."),
            ],
        },
        {
            "lesson": 2,
            "difficulty": "MEDIUM",
            "text": "According to this module, what is the single biggest security risk?",
            "options": [
                ("Human error — everyday mistakes like clicking a link or reusing a password", True,
                 "Correct — most incidents involve an ordinary human action, which is why calm habits matter more than any product."),
                ("Old printers", False,
                 "No — while any device can be a weak point, the biggest risk overall is human error."),
                ("Having too many backups", False,
                 "No — backups are a good thing; they're never the risk."),
                ("Using a router at all", False,
                 "No — routers are essential; the biggest risk is everyday human error, not the equipment."),
            ],
        },
        {
            "lesson": 2,
            "difficulty": "MEDIUM",
            "text": "Why is reusing the same password across many sites dangerous?",
            "options": [
                ("If one site is breached, attackers try that password everywhere else", True,
                 "Correct — a single leak then unlocks all your accounts; unique passwords contain the damage."),
                ("It makes websites load more slowly", False,
                 "No — password reuse has no effect on speed; the danger is that one leak unlocks everything."),
                ("It uses up storage on your device", False,
                 "No — passwords don't take meaningful storage; the risk is that a single breach spreads."),
                ("There's no real danger if the password is long", False,
                 "No — even a long password is dangerous if reused, because one breached site exposes it everywhere."),
            ],
        },
        {
            "lesson": 2,
            "difficulty": "HARD",
            "text": "An email says 'Pay this overdue invoice in the next hour or the account will be closed.' What's the safest first step?",
            "options": [
                ("Pause, and verify the request using contact details you already have", True,
                 "Correct — urgency is a pressure tactic. Slowing down and confirming another way is the safest move."),
                ("Pay immediately so the account isn't closed", False,
                 "No — acting fast is exactly what the attacker wants; the deadline exists to stop you thinking."),
                ("Reply to the email asking if it's genuine", False,
                 "Risky — if it's a scam, you're just asking the attacker, who will say yes. Verify through a channel you trust."),
                ("Click the link to see the invoice details", False,
                 "No — clicking an unexpected link is how many attacks begin; verify before you click anything."),
            ],
        },
        {
            "lesson": 2,
            "difficulty": "MEDIUM",
            "text": "Why do attackers often target small businesses, councils and schools?",
            "options": [
                ("Automated tools look for any unlocked door, and smaller organisations often have fewer defences", True,
                 "Correct — attacks are largely automated and opportunistic; being small doesn't mean being safe."),
                ("They are too small to be worth attacking", False,
                 "No — this is the dangerous myth; smaller organisations are targeted precisely because defences are often lighter."),
                ("They never hold any valuable information", False,
                 "No — they hold plenty of valuable data, from customer details to payment information."),
                ("Attackers personally choose each victim by name", False,
                 "No — most attacks are automated and untargeted, knocking on thousands of doors at once."),
            ],
        },
        {
            "lesson": 3,
            "difficulty": "MEDIUM",
            "text": "On a new router, which password is the dangerous one to leave on the factory default?",
            "options": [
                ("The admin password used to change the router's settings", True,
                 "Correct — default admin passwords are published online, so leaving it unchanged lets anyone take the router over."),
                ("The Wi-Fi password guests use to connect", False,
                 "Partly — you should change this too, but the admin password is the critical one people forget exists."),
                ("Your email password", False,
                 "No — your email password isn't set on the router; the risky default here is the router's admin password."),
                ("Neither needs changing if the box is new", False,
                 "No — both should be changed, and the admin password especially, because its defaults are publicly known."),
            ],
        },
        {
            "lesson": 3,
            "difficulty": "EASY",
            "text": "What is the main benefit of a separate 'guest' Wi-Fi network?",
            "options": [
                ("It keeps visitors' and personal devices apart from your work devices", True,
                 "Correct — if a guest device is infected, a guest network keeps that problem away from your business systems."),
                ("It makes your internet twice as fast", False,
                 "No — a guest network is about separation and safety, not speed."),
                ("It removes the need for any passwords", False,
                 "No — a guest network still uses a password; it simply separates guests from your main network."),
                ("It automatically backs up guest files", False,
                 "No — a guest network doesn't back anything up; its purpose is to keep guest devices separate."),
            ],
        },
        {
            "lesson": 3,
            "difficulty": "MEDIUM",
            "text": "When setting Wi-Fi encryption, which should you choose?",
            "options": [
                ("The most recent option your equipment supports, such as WPA3 or WPA2", True,
                 "Correct — modern encryption protects everything on the network; pick the newest your gear supports."),
                ("The oldest option, WEP, for compatibility", False,
                 "No — WEP is long broken and should be avoided; choose WPA2 or WPA3 instead."),
                ("No encryption, to keep things simple", False,
                 "No — an open network lets anyone nearby read your traffic; always use modern encryption."),
                ("It doesn't matter which you choose", False,
                 "No — it matters a great deal; older schemes like WEP are insecure, so pick the newest available."),
            ],
        },
        {
            "lesson": 3,
            "difficulty": "HARD",
            "text": "You need to log in to a work system while on free café Wi-Fi. What's the safest choice?",
            "options": [
                ("Use your phone's mobile connection or a trusted VPN instead", True,
                 "Correct — on a network you don't control, use mobile data or a trusted VPN for anything sensitive."),
                ("Go ahead — café Wi-Fi is always safe", False,
                 "No — you can't be sure who else is on public Wi-Fi or what they can see; treat it as a public space."),
                ("Just make sure the café is busy", False,
                 "No — how many customers there are tells you nothing about whether the network is safe."),
                ("Turn off your screen brightness so no one can see", False,
                 "No — the risk is the network carrying your data, not someone reading your screen."),
            ],
        },
        {
            "lesson": 4,
            "difficulty": "EASY",
            "text": "What does turning on two-factor authentication achieve?",
            "options": [
                ("A stolen password alone is no longer enough to get into the account", True,
                 "Correct — two-factor adds a second check, so a leaked password by itself won't let an attacker in."),
                ("It makes your password impossible to steal", False,
                 "No — it doesn't stop a password being stolen; it makes a stolen password insufficient on its own."),
                ("It removes the need for a password entirely", False,
                 "No — two-factor works alongside your password, adding a second step rather than replacing it."),
                ("It backs up your account", False,
                 "No — two-factor is about verifying it's really you; it isn't a backup."),
            ],
        },
        {
            "lesson": 4,
            "difficulty": "MEDIUM",
            "text": "You realise you may have entered your password into a suspicious page. What's the best thing to do?",
            "options": [
                ("Report it straight away to whoever looks after your IT or your manager", True,
                 "Correct — fast reporting turns a near-miss into a non-event; there's never trouble for reporting, only for hiding it."),
                ("Say nothing and hope nothing happens", False,
                 "No — staying quiet lets a small problem grow; quick reporting is what limits the damage."),
                ("Delete the email and carry on as normal", False,
                 "No — deleting the message doesn't undo an entered password; you need to report it so the account can be secured."),
                ("Wait a week to see if anything goes wrong", False,
                 "No — waiting gives an attacker time; report it immediately so action can be taken."),
            ],
        },
    ],
}
