"""Module 1 — Network Security Fundamentals: interactive activities and the quiz.

Content, not schema: kept as plain data so it reads like the teaching material it
is, and so the seed command stays re-runnable. Written in plain Australian
English for non-technical readers — small businesses, councils, schools.

Each lesson weaves short CONCEPT intros (with diagrams) together with inline
CHECK questions and hands-on activities (sort / inbox / spot / password /
branch), so learning and doing alternate the whole way through. Every task
carries points; a lesson's tasks sum to 10 (POINTS_PER_LESSON), so finishing the
last banks the lesson through the normal points path.

QUIZ is the end-of-module assessment. Every option carries an explanation_text —
the Adaptive Feedback Engine reads it back, so wrong options explain the
misconception, not just "no".
"""

# --------------------------------------------------------------------------
# Lessons — concept + check + activity woven together; points sum to 10.
#   concept  — a short teaching intro (optional diagram); "continue" to finish
#   check    — an inline MCQ with instant per-option feedback; solved when correct
#   sort/inbox/spot/password/branch — hands-on activities (see activities.js)
# Check option tuples are (text, is_correct, explanation). Activity config lives
# in each task's `payload`.
# --------------------------------------------------------------------------

LESSONS = [
    {
        "title": "What a network is, and what we protect",
        "reading_time_minutes": 5,
        "intro": "Meet the thing we're protecting — how your information travels, "
        "and the three questions every security decision comes back to.",
        "tasks": [
            {
                "key": "net-intro",
                "kind": "concept",
                "points": 1,
                "title": "What a network actually is",
                "diagram": "data-travels",
                "body": "<p>A <strong>network</strong> is just devices connected to "
                "share information — your laptop, the office printer, the eftpos "
                "terminal, all talking through a router to the internet. Your "
                "information is constantly <em>in transit</em> across it, which is "
                "exactly why how it travels matters.</p>",
            },
            {
                "key": "net-check",
                "kind": "check",
                "points": 2,
                "title": "Quick check",
                "question": "Which of these best describes a network?",
                "options": [
                    ("Two or more devices connected to share information", True,
                     "Exactly — from two machines to the whole internet, a network is devices connected to share information."),
                    ("A single fast computer", False,
                     "Not quite — one computer on its own isn't a network. It's the connection between devices that makes one."),
                    ("An antivirus program", False,
                     "No — antivirus protects a device; it isn't what a network is."),
                    ("Your login password", False,
                     "No — a password controls access, but it isn't the network itself."),
                ],
            },
            {
                "key": "cia-intro",
                "kind": "concept",
                "points": 2,
                "title": "The three questions security asks",
                "diagram": "cia-triad",
                "body": "<p>Keeping a network safe comes down to the "
                "<strong>CIA triad</strong> (nothing to do with spies) — the three "
                "things every security decision protects, shown here. Once they "
                "click, sort a few real situations yourself.</p>",
            },
            {
                "key": "cia-sort",
                "kind": "sort",
                "points": 3,
                "title": "Which pillar is at stake?",
                "payload": {
                    "prompt": "Tap each situation, then tap the pillar it's about. "
                    "Get all eight right to finish.",
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
                        {"id": "shoulder", "text": "A stranger reads your screen over your shoulder",
                         "bucket": "c", "why": "Information reaches someone who shouldn't see it — confidentiality."},
                        {"id": "outage", "text": "The website is knocked offline during a sale",
                         "bucket": "a", "why": "Customers can't reach it — availability."},
                    ],
                },
            },
            {
                "key": "backup-check",
                "kind": "check",
                "points": 2,
                "title": "Quick check",
                "question": "Keeping a restorable backup mainly protects which pillar?",
                "options": [
                    ("Availability — you can still get your information when you need it", True,
                     "Right — a backup means an attack or mistake doesn't cost you access to your data."),
                    ("Confidentiality — it hides the files", False,
                     "No — a backup doesn't hide anything; it ensures you can still get your data back."),
                    ("Integrity — it proves nothing changed", False,
                     "Not the main point — backups are chiefly about restoring access, which is availability."),
                    ("None — backups aren't a security control", False,
                     "No — backups are a core control; they protect availability against ransomware and mistakes."),
                ],
            },
        ],
    },
    {
        "title": "Spotting the weak points",
        "reading_time_minutes": 6,
        "intro": "Attackers walk through open doors. Learn the common ones, then "
        "inspect a scam yourself and tell a real message from a fake.",
        "tasks": [
            {
                "key": "vectors-intro",
                "kind": "concept",
                "points": 1,
                "title": "The common ways in",
                "body": "<p>Most attacks aren't clever — they rely on a busy moment. "
                "The usual ways in are <strong>phishing</strong> (messages "
                "pretending to be someone you trust), weak or reused "
                "<strong>passwords</strong>, <strong>out-of-date software</strong>, "
                "and <strong>malware</strong> such as ransomware. The biggest risk "
                "of all is ordinary <strong>human error</strong> — which is why "
                "attackers lean on urgency to stop you thinking.</p>",
            },
            {
                "key": "phishing-check",
                "kind": "check",
                "points": 2,
                "title": "Quick check",
                "question": "What is 'phishing'?",
                "options": [
                    ("A message pretending to be from someone you trust, to trick you into clicking or sharing details", True,
                     "Right — phishing impersonates a trusted sender, and it's the most common way organisations are attacked."),
                    ("A way to speed up your internet", False,
                     "No — phishing has nothing to do with speed; it's a form of deception."),
                    ("A tool that backs up your files", False,
                     "No — that's a backup. Phishing is a scam message designed to trick you."),
                    ("A setting on your router", False,
                     "No — phishing arrives as a message; it isn't a router setting."),
                ],
            },
            {
                "key": "email-anatomy",
                "kind": "concept",
                "points": 1,
                "title": "Anatomy of a scam email",
                "diagram": "phishing-email",
                "body": "<p>Almost every phishing email gives itself away in the "
                "same few places: a <strong>lookalike sender</strong>, a "
                "manufactured <strong>deadline</strong>, and a <strong>link</strong> "
                "that doesn't go where it claims. Here's one annotated — then you'll "
                "find the tells yourself.</p>",
            },
            {
                "key": "phishing-inbox",
                "kind": "inbox",
                "points": 3,
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
                        {"id": "greeting", "zone": "Body",
                         "text": "Dear Valued Customer,",
                         "bad": True,
                         "why": "A generic greeting — a real sender who knows you usually uses your name."},
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
                "points": 2,
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
            {
                "key": "urgency-check",
                "kind": "check",
                "points": 1,
                "title": "Quick check",
                "question": "An email demands you pay a changed invoice within the hour. Best first step?",
                "options": [
                    ("Pause and verify by phoning a number you already have", True,
                     "Correct — urgency plus changed bank details is the classic invoice scam. Verify through a channel you trust."),
                    ("Pay quickly so nothing gets cut off", False,
                     "No — acting fast is exactly what the attacker wants; the deadline exists to stop you thinking."),
                    ("Reply and ask if it's genuine", False,
                     "Risky — if it's a scam you're just asking the attacker, who'll say yes."),
                    ("Click the link to check the details", False,
                     "No — an unexpected link is how many attacks begin; verify before you click."),
                ],
            },
        ],
    },
    {
        "title": "Locking the front door",
        "reading_time_minutes": 6,
        "intro": "The router is the front door to everything. Build a password "
        "worth trusting, then sort the habits that keep it shut.",
        "tasks": [
            {
                "key": "router-intro",
                "kind": "concept",
                "points": 1,
                "title": "Your router is the front door",
                "body": "<p>Almost everything you do online passes through the "
                "<strong>router</strong> — the box that connects your workplace to "
                "the internet. It has two passwords people mix up: the "
                "<strong>Wi-Fi password</strong> to join, and the "
                "<strong>admin password</strong> that changes its settings.</p>",
            },
            {
                "key": "admin-pw-check",
                "kind": "check",
                "points": 2,
                "title": "Quick check",
                "question": "Which password is dangerous to leave on the factory default?",
                "options": [
                    ("The admin password that changes the router's settings", True,
                     "Right — default admin passwords are published online, so anyone who reaches the router can take it over."),
                    ("The guest Wi-Fi password", False,
                     "Change that too, but the admin password is the critical one people forget exists."),
                    ("Your email password", False,
                     "Your email password isn't set on the router — the risky default is the router's admin password."),
                    ("Neither, if the box is new", False,
                     "No — both should be changed, the admin one especially, because its default is publicly known."),
                ],
            },
            {
                "key": "password-builder",
                "kind": "password",
                "points": 3,
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
                "key": "wifi-intro",
                "kind": "concept",
                "points": 1,
                "title": "Encryption, guests and updates",
                "body": "<p>Three more quick wins: choose modern <strong>Wi-Fi "
                "encryption</strong> (WPA3 or WPA2, never old WEP); run a separate "
                "<strong>guest network</strong> so visitors' devices stay away from "
                "your work ones; and turn on <strong>automatic updates</strong> for "
                "the router and everything on it.</p>",
            },
            {
                "key": "wifi-sort",
                "kind": "sort",
                "points": 1,
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
            {
                "key": "cafe-check",
                "kind": "check",
                "points": 2,
                "title": "Quick check",
                "question": "You must log in to a work system on free café Wi-Fi. Safest choice?",
                "options": [
                    ("Use your phone's mobile data or a trusted VPN instead", True,
                     "Correct — on a network you don't control, use mobile data or a trusted VPN for anything sensitive."),
                    ("Go ahead — café Wi-Fi is fine", False,
                     "No — you can't be sure who else is on it or what they can see. Treat it as a public space."),
                    ("Check the café is busy first", False,
                     "No — how many customers are in tells you nothing about whether the network is safe."),
                    ("Just lower your screen brightness", False,
                     "No — the risk is the network carrying your data, not someone reading your screen."),
                ],
            },
        ],
    },
    {
        "title": "A week at Docklands Dental",
        "reading_time_minutes": 5,
        "intro": "Put it all together. Make the calls a real small business faces, "
        "see where each one leads, and lock in the habits that matter most.",
        "tasks": [
            {
                "key": "capstone-intro",
                "kind": "concept",
                "points": 2,
                "title": "Putting it together",
                "body": "<p>You've met the ideas: what a network is, the three "
                "pillars, the common weak points, and the front door. The last "
                "piece is the habit that catches what everything else misses — "
                "<strong>two-factor authentication</strong>, a second check so a "
                "stolen password alone isn't enough. Let's run a real week.</p>",
            },
            {
                "key": "twofactor-check",
                "kind": "check",
                "points": 2,
                "title": "Quick check",
                "question": "What does turning on two-factor authentication achieve?",
                "options": [
                    ("A stolen password alone is no longer enough to get in", True,
                     "Right — a second check means a leaked password by itself won't let an attacker into your account."),
                    ("It makes your password impossible to steal", False,
                     "No — it doesn't stop a password being stolen; it makes a stolen password insufficient on its own."),
                    ("It replaces your password entirely", False,
                     "No — two-factor works alongside your password, adding a second step."),
                    ("It backs up your account", False,
                     "No — two-factor verifies it's really you; it isn't a backup."),
                ],
            },
            {
                "key": "capstone-branch",
                "kind": "branch",
                "points": 4,
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
                                 "feedback": "Staying quiet lets a small problem grow. Fast reporting limits the damage."},
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
                            "text": "Thursday. Setting up a new laptop, you're offered two-factor "
                            "authentication on the practice email. It's a couple of extra minutes.",
                            "choices": [
                                {"label": "Skip it — it's fiddly and everyone's busy", "to": "n3bad",
                                 "outcome": "bad",
                                 "feedback": "Skipping it leaves a stolen password as the only lock on the door."},
                                {"label": "Turn it on now", "to": "n4",
                                 "outcome": "good",
                                 "feedback": "Good — a stolen password alone now won't be enough."},
                            ],
                        },
                        "n3bad": {
                            "text": "A month later a reused password leaks from another site — and it opens "
                            "the practice email too.",
                            "choices": [{"label": "See the better path", "to": "n4"}],
                        },
                        "n4": {
                            "text": "Friday. Reviewing the week, which single habit would have prevented "
                            "the most harm?",
                            "choices": [
                                {"label": "Two-factor authentication on email", "to": "end",
                                 "outcome": "good",
                                 "feedback": "Yes — a stolen password alone wouldn't have been enough to get in."},
                                {"label": "A faster internet plan", "to": "n4",
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
            {
                "key": "report-check",
                "kind": "check",
                "points": 2,
                "title": "Quick check",
                "question": "You realise you entered your password into a suspicious page. What first?",
                "options": [
                    ("Report it straight away to whoever looks after your IT", True,
                     "Correct — fast reporting turns a near-miss into a non-event. There's never trouble for reporting, only for hiding it."),
                    ("Say nothing and hope it's fine", False,
                     "No — staying quiet lets a small problem grow. Quick reporting limits the damage."),
                    ("Delete the page from your history", False,
                     "No — that doesn't undo an entered password; it needs reporting so the account can be secured."),
                    ("Wait a week to see if anything happens", False,
                     "No — waiting just gives an attacker time. Report it now."),
                ],
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
        # ---- Lesson 1 (deeper) ----
        {
            "lesson": 1,
            "difficulty": "MEDIUM",
            "text": "Your information is 'in transit' when it is…",
            "options": [
                ("Moving across the network — for example, attached to an email on its way to someone", True,
                 "Correct — in transit means the information is travelling, which is when it can be intercepted if unprotected."),
                ("Saved on a hard drive and switched off", False,
                 "That's 'at rest' — stored, not moving."),
                ("Printed on paper in a drawer", False,
                 "That's a physical copy at rest, not data in transit."),
                ("Deleted from your computer", False,
                 "Deleted data isn't 'in transit'; in transit means actively moving across a network."),
            ],
        },
        {
            "lesson": 1,
            "difficulty": "EASY",
            "text": "Putting a password on a spreadsheet of customer details mainly protects…",
            "options": [
                ("Confidentiality — keeping it from people who shouldn't see it", True,
                 "Correct — restricting who can open it is a confidentiality control."),
                ("Availability — keeping it online", False,
                 "No — a password doesn't keep it available; it limits who can read it."),
                ("Integrity — proving it wasn't changed", False,
                 "Not the main point — a password limits access, which is confidentiality."),
                ("Nothing — spreadsheets can't be protected", False,
                 "No — a password is a real, if basic, confidentiality control."),
            ],
        },
        {
            "lesson": 1,
            "difficulty": "MEDIUM",
            "text": "Which of these is NOT one of the three things the CIA triad protects?",
            "options": [
                ("Speed", True,
                 "Correct — speed isn't part of it. The three are Confidentiality, Integrity and Availability."),
                ("Confidentiality", False,
                 "That IS one of the three — keeping information from the wrong eyes."),
                ("Integrity", False,
                 "That IS one of the three — information not being tampered with."),
                ("Availability", False,
                 "That IS one of the three — information being there when you need it."),
            ],
        },
        # ---- Lesson 2 (deeper) ----
        {
            "lesson": 2,
            "difficulty": "EASY",
            "text": "Ransomware is a type of…",
            "options": [
                ("Malware that locks up your files and demands payment to unlock them", True,
                 "Correct — and tested backups are the defence that let you recover without paying."),
                ("Strong password", False,
                 "No — ransomware is harmful software, not a password."),
                ("Wi-Fi encryption setting", False,
                 "No — that's unrelated; ransomware is malware that holds files hostage."),
                ("Backup tool", False,
                 "The opposite — backups are your defence against ransomware."),
            ],
        },
        {
            "lesson": 2,
            "difficulty": "MEDIUM",
            "text": "An email from 'service@auspost-delivery.info' claims to be Australia Post. The clearest tell is…",
            "options": [
                ("The domain isn't auspost.com.au — it's a lookalike", True,
                 "Correct — the real giveaway is the sender's domain, a lookalike designed to pass a quick glance."),
                ("It mentions a parcel", False,
                 "Plenty of genuine messages mention parcels — that alone isn't a tell."),
                ("It's written in English", False,
                 "Language isn't the tell; the lookalike domain is."),
                ("It arrived in the morning", False,
                 "Timing tells you nothing about whether it's genuine."),
            ],
        },
        # ---- Lesson 3 (deeper) ----
        {
            "lesson": 3,
            "difficulty": "MEDIUM",
            "text": "You notice your Wi-Fi is set to 'WEP'. What should you do?",
            "options": [
                ("Switch to WPA3 or WPA2 — WEP has been broken for years", True,
                 "Correct — WEP is insecure and easily cracked; move to the newest option your gear supports."),
                ("Leave it — WEP is the most secure", False,
                 "No — WEP is the oldest and broken; it's the least secure."),
                ("Turn encryption off to keep things simple", False,
                 "No — an open network lets anyone nearby read your traffic."),
                ("Nothing — encryption doesn't matter on Wi-Fi", False,
                 "It matters a great deal; unencrypted Wi-Fi exposes everything on it."),
            ],
        },
        {
            "lesson": 3,
            "difficulty": "MEDIUM",
            "text": "Why is it worth installing software updates promptly?",
            "options": [
                ("They often fix security holes that attackers are actively exploiting", True,
                 "Correct — an update usually closes a known hole; the gap before you install it is exactly what attackers target."),
                ("They always make the device faster", False,
                 "Speed isn't the point — the security fixes are."),
                ("They change the look of the screen", False,
                 "Appearance is incidental; the security fixes are why prompt updates matter."),
                ("They aren't important if you have antivirus", False,
                 "No — antivirus doesn't patch the holes updates fix; you need both."),
            ],
        },
        {
            "lesson": 3,
            "difficulty": "HARD",
            "text": "What makes a password strongest?",
            "options": [
                ("Length — a dozen or more characters, such as a few unrelated words", True,
                 "Correct — length beats complexity; a long passphrase is both strong and memorable."),
                ("Swapping a couple of letters for symbols in a short word", False,
                 "No — 'P@ss1' is short and guessable; substitutions don't rescue a short password."),
                ("Using the same strong password everywhere", False,
                 "No — reuse means one leak unlocks everything, however strong the password."),
                ("Your pet's name so you won't forget it", False,
                 "No — personal details are exactly what attackers guess first."),
            ],
        },
        # ---- Lesson 4 (deeper) ----
        {
            "lesson": 4,
            "difficulty": "MEDIUM",
            "text": "A supplier emails that their bank account has changed. The safest way to verify is…",
            "options": [
                ("Phone them on a number you already have on file", True,
                 "Correct — confirm a change of details through a channel you already trust, not one from the email."),
                ("Reply to the email and ask them to confirm", False,
                 "Risky — if the email is a scam, you're just asking the attacker."),
                ("Use the phone number printed in the email", False,
                 "No — a scammer supplies their own number; use details you already hold."),
                ("Just pay it — suppliers don't lie about bank details", False,
                 "No — changed bank details is the single most common invoice scam."),
            ],
        },
        {
            "lesson": 4,
            "difficulty": "EASY",
            "text": "A colleague admits they clicked a phishing link. The best response is…",
            "options": [
                ("Thank them for speaking up and report it so the account can be secured", True,
                 "Correct — a blame-free, fast report is what limits the damage; punishing it just drives the next one into hiding."),
                ("Tell them off so they're more careful next time", False,
                 "No — blame makes people hide mistakes, which is far more dangerous."),
                ("Tell them to keep it quiet", False,
                 "No — silence lets a small problem grow into a large one."),
                ("Do nothing unless something obviously breaks", False,
                 "No — by the time damage shows, the attacker has had free rein."),
            ],
        },
        {
            "lesson": 4,
            "difficulty": "MEDIUM",
            "text": "What lets a business recover from ransomware without paying the criminals?",
            "options": [
                ("Recent backups that have been tested and can actually be restored", True,
                 "Correct — a good backup means you can restore and carry on rather than negotiate."),
                ("A faster internet connection", False,
                 "No — speed does nothing against ransomware."),
                ("Paying quickly for a discount", False,
                 "No — paying is no guarantee of recovery and marks you as willing to pay again."),
                ("Turning the computer off and on again", False,
                 "No — that won't undo the encryption ransomware applies."),
            ],
        },
        {
            "lesson": 4,
            "difficulty": "MEDIUM",
            "text": "If you could protect only one account with two-factor authentication first, which should it be?",
            "options": [
                ("Your email — it can reset the passwords of most of your other accounts", True,
                 "Correct — email is the master key; protecting it protects everything it can reset."),
                ("A rarely used shopping site", False,
                 "Lower value — start with the account that unlocks the others."),
                ("A news website with no login details", False,
                 "There's little to protect there; email matters far more."),
                ("Whichever you use least", False,
                 "The opposite — protect the highest-value account, your email, first."),
            ],
        },
        {
            "lesson": 4,
            "difficulty": "EASY",
            "text": "A password manager mainly helps by…",
            "options": [
                ("Letting you use a different strong password everywhere without memorising them", True,
                 "Correct — it remembers unique strong passwords for you, so one leaked site can't unlock the rest."),
                ("Making your internet faster", False,
                 "No — it has nothing to do with speed."),
                ("Sharing your passwords with colleagues", False,
                 "No — that would undermine security, not help it."),
                ("Removing the need for any password", False,
                 "No — it manages passwords; it doesn't abolish them."),
            ],
        },
    ],
}
